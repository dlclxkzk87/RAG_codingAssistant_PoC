from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from preprocess import preprocess_text


llm = Ollama(
    model="qwen2.5-coder:7b",
    temperature=0
)

embedding = OllamaEmbeddings(
    model="bge-m3:latest"
)

def load_documents(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

raw_text = load_documents("./data/docs/internal_guide.txt")

processed = preprocess_text(raw_text)

documents = []

for text in processed["rules"]:
    documents.append(
        Document(page_content=text, metadata={"type": "rule"})
    )

for text in processed["codes"]:
    documents.append(
        Document(page_content=text, metadata={"type": "code"})
    )

for text in processed["explains"]:
    documents.append(
        Document(page_content=text, metadata={"type": "explain"})
    )

vectorstore = FAISS.from_documents(
    documents=documents,
    embedding=embedding
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

prompt = PromptTemplate.from_template(
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

rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

def ask_rag(question: str) -> str:
    return rag_chain.invoke(question)
