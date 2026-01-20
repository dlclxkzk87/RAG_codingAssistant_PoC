# rag_app.py
# LCEL 기반 RAG (langchain_core + langchain_community)
# RetrievalQA 미사용

from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from preprocess import preprocess_text


# 1. LLM / Embedding 설정
# RAG 전용 LLM (문서 기반 답변만)
rag_llm = Ollama(
    model="llama3",
    temperature=0
)

# 일반 설명 전용 LLM (문서 미참조)
general_llm = Ollama(
    model="llama3",
    temperature=0.2
)

# 임베딩 모델
embedding = OllamaEmbeddings(
    model="bge-m3:latest"
)


# 2. 문서 로딩 & 전처리
def load_raw_text(file_path: str) -> str:
    """
    내부 문서를 파일에서 로딩
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


raw_text = load_raw_text("./data/docs/internal_guide.txt")
processed = preprocess_text(raw_text)

documents: list[Document] = []

for text in processed["rules"]:
    documents.append(
        Document(
            page_content=text,
            metadata={"type": "rule"}
        )
    )

for text in processed["codes"]:
    documents.append(
        Document(
            page_content=text,
            metadata={"type": "code"}
        )
    )

for text in processed["explains"]:
    documents.append(
        Document(
            page_content=text,
            metadata={"type": "explain"}
        )
    )


# 3. Vector DB & Retriever (FAISS)

vectorstore = FAISS.from_documents(
    documents=documents,
    embedding=embedding
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# 4. RAG 전용 프롬프트 (강제 거부 규칙 포함)

rag_prompt = PromptTemplate.from_template(
    """
당신은 사내 폐쇄망 AI 코딩 어시스턴트입니다.

아래 제공된 내부 문서(context)에 명시된 내용만 근거로 답변하세요.
문서에 해당 내용이 없거나 관련 정보를 찾을 수 없는 경우,
반드시 다음 문장으로만 답변하세요:

"제공된 내부 문서에 해당 내용이 없어 답변할 수 없습니다."

[내부 문서]
{context}

[질문]
{question}

[답변]
"""
)


# 5. LCEL 기반 RAG 체인

rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | rag_prompt
    | rag_llm
    | StrOutputParser()
)


# 6. 일반 설명 전용 함수

def general_llm_answer(question: str) -> str:
    prompt = f"""
다음 설명은 사내 내부 문서를 근거로 하지 않은
일반적인 기술 지식에 기반한 참고 설명입니다.

반드시 한국어로만 설명하세요.
코드가 포함될 경우 간단한 설명 위주로 작성하세요.

질문:
{question}

설명:
"""
    return general_llm.invoke(prompt)


# 7. Streamlit에서 호출하는 API

def ask_rag(question: str, allow_general: bool = False) -> str:
    rag_result = rag_chain.invoke(question)

    if "제공된 내부 문서에 해당 내용이 없어" in rag_result:
        if allow_general is not True:
            return (
                rag_result
                + "\n\n"
                + '일반적인 설명이 필요하시면 "일반 설명"이라고 입력해 주세요.'
            )
        else:
            return general_llm_answer(question)

    return rag_result
