# RAG Coding Assistant PoC

## 프로젝트 한 줄 요약
본 프로젝트는 **폐쇄망 환경에서 동작하는 로컬 PC 기반 RAG 코딩 어시스턴트 PoC**입니다.

외부 API나 인터넷 연결 없이,
내부 문서와 코드를 기반으로 질의응답이 가능하도록 구현되었습니다.

---

## PoC 목적
- 폐쇄망 / 데이터 안심존 환경에서 AI 활용 가능성 검증
- RAG 기반 코딩·기술 문서 질의응답 구조 검증
- 로컬 PC 단독 실행 PoC 아키텍처 제시

---

## 핵심 구성 요소
[내부 문서 / 코드]
↓
[Chunk 분할 + 임베딩]
↓
[FAISS Vector DB]
↓
[질문 → 문서 검색]
↓
[Ollama LLM 응답 생성]


---

## 기술 스택

| 구분 | 내용 |
|---|---|
| Language | Python |
| LLM | Ollama (로컬 LLM) |
| RAG | LangChain |
| Vector DB | FAISS |
| 실행 환경 | Local PC (폐쇄망) |

---

## 실행 흐름 (PoC 기준)

1. 내부 문서 준비 (`data/docs`)
2. 문서 임베딩 실행  
   ```bash
   python ingest.py
