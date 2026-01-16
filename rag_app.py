from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama

# 1. 문서 로딩
loader = TextLoader("data/docs/sample.txt", encoding="utf-8")
documents = loader.load()

# 2. 문서 분할
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
docs = text_splitter.split_documents(documents)

# 3. 임베딩 모델 (Ollama 사용)
embeddings = OllamaEmbeddings(model="bge-m3:latest")

# 4. Vector DB 생성
vectorstore = FAISS.from_documents(docs, embeddings)

# 5. LLM 로딩
llm = Ollama(model="qwen2.5-coder:7b")

# 6. 질문
query = "python while문에서 무한루프 문제가 발생할 경우 빠져나오는 방법을 알려줘"

# 7. 문서 검색
docs = vectorstore.similarity_search(query, k=2)

# 8. 검색 결과 + 질문 결합
context = "\n".join([doc.page_content for doc in docs])
prompt = f"""
아래 문서를 참고해서 질문에 답해줘.

문서:
{context}

질문:
{query}
"""

# 9. LLM 호출
response = llm.invoke(prompt)
print(response)
