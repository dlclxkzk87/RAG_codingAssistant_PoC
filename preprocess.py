import re

def preprocess_text(raw_text: str):
    """
    Markdown 기반 비정형 문서를
    rules / codes / explains 로 분리하는 전처리 함수
    """

    lines = raw_text.splitlines()

    rules = []
    explains = []
    codes = []

    code_block = False
    code_buffer = []

    rule_pattern = re.compile(r"^\d+[-\.]\d+|\(\d+\)")  # 1-1, 1.1, (1) 등

    for line in lines:
        stripped = line.strip()

        # 코드 블록 시작/종료 탐지 (``` 또는 ```python 등)
        if stripped.startswith("```"):
            if not code_block:
                code_block = True
                code_buffer = []
            else:
                code_block = False
                if code_buffer:
                    codes.append("\n".join(code_buffer))
                    code_buffer = []
            continue

        # 코드 블록 내부
        if code_block:
            code_buffer.append(line)
            continue

        # 규칙 탐지
        if rule_pattern.match(stripped):
            rules.append(stripped)
            continue

        # 일반 설명
        if stripped:
            explains.append(stripped)

    # 코드 블록이 닫히지 않은 경우 보호 로직
    if code_block and code_buffer:
        codes.append("\n".join(code_buffer))

    return {
        "rules": rules,
        "codes": codes,
        "explains": explains
    }
