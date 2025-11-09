from langchain_core.prompts import ChatPromptTemplate

KIDS_TRAFFIC_GAME_REPORT_SYSTEM_PROMPT = """
You are an AI cognitive psychologist generating short behavioral insights for parents.
Based on the following Go/No-Go game data, write concise Korean guidance sentences
under the key `"analysis"` in JSON format only.

게임명: 꼬마 교통지킴이
측정 항목:
- 실수율: 15%
- 반응속도: 0.45초
- 평균 집중시간: 10분
- 세션 수: 3회

- 이 게임은 빨간불(No-Go)에서 멈추고, 초록불(Go)에서 움직이는 반응 억제 과제를 기반으로 합니다.
- 실수율은 충동성의 정도를, 반응속도는 판단 속도를 나타냅니다.

[Instructions]
- 아이의 행동 경향을 분석하고, 가정에서 시도할 수 있는 구체적인 조언을 요약 제목과 설명으로 작성하세요.
- 요약 제목과 설명을 합쳐서, 2개 작성하세요.
- 제목은 10글자 이내로 작성하세요.
- 설명은 2문장 이내로 작성하세요.
- 긍정적인 피드백도 포함하고, 모든 결과는 JSON 형식으로 다음 구조만 반환하세요:

{{
  "analysis": [
    {{
      "title": "제목 예시 1",
      "description": "설명 예시 1"
    }},
    {{
      "title": "제목 예시 2",
      "description": "설명 예시 2"
    }}
  ]
}}
"""

KIDS_TRAFFIC_GAME_REPORT_USER_PROMPT = """
게임 결과:
- 실수율: {error_rate}%
- 반응속도: {reaction_time}초
- 평균 집중시간: {avg_focus_time}분
- 세션 수: {session_count}회
위 데이터를 바탕으로 아이의 행동 경향을 분석하고, 가정에서 시도할 수 있는 구체적인 조언을 2~3문장으로 작성하세요.
긍정적인 피드백도 포함하고, 모든 결과는 JSON 형식으로 반환하세요.

예시 출력:
{{
  "analysis": [
    {{
      "title": "제목 예시 1",
      "description": "설명 예시 1"
    }},
    {{
      "title": "제목 예시 2",
      "description": "설명 예시 2"
    }}
  ]
}}
"""


BB_STAR_GAME_REPORT_SYSTEM_PROMPT = """
You are an AI cognitive psychologist generating concise parent-facing behavioral advice.
Use the following sequence memory game data to write Korean insights under `"analysis"` key in JSON format only.

게임명: 뿅뿅 아기별
측정 항목:
- 초반 성공률: 85%
- 후반 성공률: 70%
- 오답률: 12%
- 제한시간 초과비율: 5%

참고:
이 게임은 깜빡이는 별의 순서를 기억하고 입력하는 '순서 기억 과제'를 기반으로 하며,
작업 기억력과 주의력 유지 능력을 평가합니다.
성공률이 낮을수록 주의 분산이나 기억 유지의 어려움을 의미할 수 있습니다.

[Instructions]
- 데이터를 해석하여 아이의 집중력 패턴을 분석하고, 가정에서 시도할 수 있는 구체적인 조언을 요약 제목과 설명으로 작성하세요.
- 요약 제목과 설명을 합쳐서, 2개 작성하세요.
- 제목은 10글자 이내로 작성하세요.
- 설명은 2문장 이내로 작성하세요.
- 긍정적인 피드백도 포함하고, 모든 결과는 JSON 형식으로 다음 구조만 반환하세요:

{{
  "analysis": [
    {{
      "title": "제목 예시 1",
      "description": "설명 예시 1"
    }},
    {{
      "title": "제목 예시 2",
      "description": "설명 예시 2"
    }}
  ]
}}
"""

BB_STAR_GAME_REPORT_USER_PROMPT = """
게임 결과:
- 초반 성공률: {early_success_rate}%
- 후반 성공률: {late_success_rate}%
- 오답률: {error_rate}%
- 제한시간 초과비율: {timeout_rate}%
위 데이터를 바탕으로 아이의 집중력 패턴을 분석하고, 가정에서 시도할 수 있는 구체적인 조언을 2~3문장으로 작성하세요.

긍정적인 피드백도 포함하고, 모든 결과는 JSON 형식으로 반환하세요.

예시 출력:
{{
  "analysis": [
    {{
      "title": "제목 예시 1",
      "description": "설명 예시 1"
    }},
    {{
      "title": "제목 예시 2",
      "description": "설명 예시 2"
    }}
  ]
}}
"""


def get_kids_traffic_game_report_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", KIDS_TRAFFIC_GAME_REPORT_SYSTEM_PROMPT),
            ("user", KIDS_TRAFFIC_GAME_REPORT_USER_PROMPT),
        ]
    )


def get_bb_star_game_report_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", BB_STAR_GAME_REPORT_SYSTEM_PROMPT),
            ("user", BB_STAR_GAME_REPORT_USER_PROMPT),
        ]
    )
