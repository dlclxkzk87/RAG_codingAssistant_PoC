# 폐쇄망 로컬 AI 코딩 어시스턴트 (LCEL 기반 RAG PoC)

본 프로젝트는 **폐쇄망 환경에서 로컬 LLM과 RAG를 활용한 코딩 어시스턴트 PoC**를 목적으로 

LangChain의 **LCEL(LangChain Expression Language)** 구조를 사용하여 문서 기반 응답과 일반 LLM 응답을 명확히 분리하는 것을 목표로 진행하였습니다.

---

## 1. 프로젝트 목적

- 폐쇄망 환경에서 외부 API 호출 없이 AI 코딩 어시스턴트 구축
- 내부 문서 기반 응답(RAG) 신뢰성 검증
- 문서가 없는 경우 **답변을 거부**하는 구조 설계
- 사용자가 명시적으로 요청한 경우에만 일반 설명 제공

---

## 2. 핵심 특징

- LCEL 기반 RAG 체인 구성
- 내부 문서 우선 응답
- 문서가 없으면 답변 거부
- 선택형 일반 설명 (사용자 요청 시)
- FAISS 기반 로컬 Vector DB
- Ollama 기반 로컬 LLM 실행

---

## 3. 시스템 구성

PoC의 시스템 흐름 :

[Streamlit UI] → [ask_rag API]  → [Retriever (FAISS)]  → [LCEL RAG Chain]  → [Local LLM (Ollama)]

기술스택 : 
- UI: Streamlit
- Retrieval: FAISS Vector DB
- Chain: LangChain LCEL
- LLM: Ollama (로컬 실행)

---

## 4. 프로젝트 구조

프로젝트 디렉터리 구조
```bash
project/
├─ app.py # Streamlit UI
├─ rag_app.py # LCEL 기반 RAG 로직
├─ preprocess.py # 비정형 문서 전처리
├─ requirements.txt
├─ README.md
└─ data/
└─ internal_guide.txt # 내부 문서 샘플
```

---

## 5. 실행 환경

- Python 3.10 이상
- Ollama (로컬 LLM 런타임)
- OS: Windows / macOS / Linux

---

## 6. 설치 방법

### 1. 가상환경 생성 및 활성화

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS / Linux 

deactivate # 가상환경 종료 시 
```
### 2. 패키지 설치
```
pip install -r requirements.txt
```
---

## 7. Ollama 모델 준비
```bash
ollama pull llama3
ollama pull bge-m3
ollama pull qwen2.5-coder:7b
```

설치된 모델 확인: 
```bash
ollama list
```

---

## 8. 실행 방법

아래 명령으로 Streamlit 앱을 실행.
```bash
streamlit run app.py
```
---

## 9. 동작 방식
(1) 내부 문서에 있는 질문 : 내부 문서를 근거로 답변 생성

(2) 내부 문서에 없는 질문
```bash
제공된 내부 문서에 해당 내용이 없어 답변할 수 없습니다.

일반적인 설명이 필요하시면 "일반 설명"이라고 입력해 주세요.
```
(3) 사용자가 "일반 설명" 입력 : 내부 문서와 무관한 일반 기술 설명 제공 (한국어)

---
