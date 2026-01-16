from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama


# RAG 초기화 (1회)
loader = TextLoader("data/docs/sample.txt", encoding="utf-8")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
docs = text_splitter.split_documents(documents)

embeddings = OllamaEmbeddings(model="bge-m3:latest")
vectorstore = FAISS.from_documents(docs, embeddings)

llm = Ollama(model="qwen2.5-coder:7b")


# 질문 함수 (UI에서 호출)
def ask_rag(query: str) -> str:
    docs = vectorstore.similarity_search(query, k=2)
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
아래 문서를 참고해서 질문에 답해줘.

문서:
{context}

질문:
{query}
"""

    response = llm.invoke(prompt)
    return response
