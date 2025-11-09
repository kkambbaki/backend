import json
import time
from abc import ABC, abstractmethod
from typing import Optional

from django.conf import settings

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import ValidationError

from .models import GameReportAdviceResponse
from .prompt import get_bb_star_game_report_prompt, get_kids_traffic_game_report_prompt
from .provider import get_chat_model

LLM_PROVIDER = settings.LLM_PROVIDER


class ReportAdviceGenerator(ABC):
    def __init__(
        self,
        provider_name: Optional[str] = None,
        temperature: float = 0.7,
        max_retries: int = 5,
    ):
        """
        Args:
            provider_name: LLM provider name (ollama, openai, gemini)
            temperature: Sampling temperature
            max_retries: Maximum number of retries on failure
        """
        self.provider_name = provider_name or LLM_PROVIDER
        self.temperature = temperature
        self.max_retries = max_retries

        # LLM Chat 모델 초기화
        self.llm = get_chat_model(self.provider_name, self.temperature)

        # 프롬프트 및 파서 초기화
        self.prompt = self.get_prompt()
        self.parser = JsonOutputParser(pydantic_object=self.get_response_model())

        # 체인 생성
        self.chain = self.prompt | self.llm | self.parser

        @abstractmethod
        def generate_advice(self, report_data: dict) -> list:
            """리포트 데이터를 기반으로 조언 생성

            Args:
                report_data: 리포트 정보를 담은 딕셔너리

            Returns:
                생성된 조언 문자열 리스트
            """
            pass

        @abstractmethod
        def get_prompt(self):
            """특정 리포트 유형에 대한 프롬프트 템플릿을 가져옵니다.

            Returns:
                ChatPromptTemplate 인스턴스
            """
            pass

        @abstractmethod
        def get_response_model(self):
            """LLM 응답을 파싱하기 위한 Pydantic 모델을 가져옵니다.

            Returns:
                Pydantic 모델 클래스
            """
            pass


class KidsTrafficGameReportAdviceGenerator(ReportAdviceGenerator):
    """꼬마 교통지킴이 게임 리포트 조언 생성기"""

    def get_prompt(self) -> ChatPromptTemplate:
        """꼬마 교통지킴이 게임 리포트에 대한 프롬프트 템플릿을 가져옵니다."""
        return get_kids_traffic_game_report_prompt()

    def get_response_model(self):
        """LLM 응답을 파싱하기 위한 Pydantic 모델을 가져옵니다."""
        return GameReportAdviceResponse

    def generate_advice(self, report_data: dict) -> list:
        """
        꼬마 교통지킴이 게임 리포트 데이터를 기반으로 조언 생성

        Args:
            report_data: 리포트 정보를 담은 딕셔너리, 다음 키 포함:
                - error_rate: 실수율 (%)
                - reaction_time: 반응속도 (초)
                - avg_focus_time: 평균 집중시간 (분)
                - session_count: 세션 수

        Returns:
            생성된 조언 딕셔너리 리스트, 각 딕셔너리는 'title'과 'description' 키를 포함
        """
        for attempt in range(self.max_retries):
            try:
                result = self.chain.invoke(
                    {
                        "error_rate": report_data.get("error_rate", 0),
                        "reaction_time": report_data.get("reaction_time", 0),
                        "avg_focus_time": report_data.get("avg_focus_time", 0),
                        "session_count": report_data.get("session_count", 0),
                    }
                )

                response = GameReportAdviceResponse(**result)

                return [{"title": item.title, "description": item.description} for item in response.analysis]

            except ValidationError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise Exception(f"Validation failed after {self.max_retries} attempts: {e}")

            except json.JSONDecodeError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise Exception(f"JSON parsing failed after {self.max_retries} attempts: {e}")

            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise Exception(f"Advice generation failed after {self.max_retries} attempts: {e}")

        raise Exception(f"Failed to generate advice after {self.max_retries} attempts")


class BBStarGameReportAdviceGenerator(ReportAdviceGenerator):
    """뿅뿅 아기별 게임 리포트 조언 생성기"""

    def get_prompt(self) -> ChatPromptTemplate:
        """뿅뿅 아기별 게임 리포트에 대한 프롬프트 템플릿을 가져옵니다."""
        return get_bb_star_game_report_prompt()

    def get_response_model(self):
        """LLM 응답을 파싱하기 위한 Pydantic 모델을 가져옵니다."""
        return GameReportAdviceResponse

    def generate_advice(self, report_data: dict) -> list:
        """
        뿅뿅 아기별 게임 리포트 데이터를 기반으로 조언 생성

        Args:
            report_data: 리포트 정보를 담은 딕셔너리, 다음 키 포함:
                - early_success_rate: 초반 성공률 (%)
                - late_success_rate: 후반 성공률 (%)
                - error_rate: 오답률 (%)
                - timeout_rate: 제한시간 초과비율 (%)

        Returns:
            생성된 조언 딕셔너리 리스트, 각 딕셔너리는 'title'과 'description' 키를 포함
        """
        for attempt in range(self.max_retries):
            try:
                result = self.chain.invoke(
                    {
                        "early_success_rate": report_data.get("early_success_rate", 0),
                        "late_success_rate": report_data.get("late_success_rate", 0),
                        "error_rate": report_data.get("error_rate", 0),
                        "timeout_rate": report_data.get("timeout_rate", 0),
                    }
                )

                response = GameReportAdviceResponse(**result)

                return [{"title": item.title, "description": item.description} for item in response.analysis]

            except ValidationError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise Exception(f"Validation failed after {self.max_retries} attempts: {e}")

            except json.JSONDecodeError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise Exception(f"JSON parsing failed after {self.max_retries} attempts: {e}")

            except Exception as e:
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    continue
                raise Exception(f"Advice generation failed after {self.max_retries} attempts: {e}")

        raise Exception(f"Failed to generate advice after {self.max_retries} attempts")
