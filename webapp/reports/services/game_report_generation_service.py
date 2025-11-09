import logging

from django.db import transaction

from games.choices import GameCodeChoice
from reports.llm.generator import (
    BBStarGameReportAdviceGenerator,
    KidsTrafficGameReportAdviceGenerator,
)
from reports.models import GameReport, GameReportAdvice

logger = logging.getLogger(__name__)


class GameReportGenerationService:
    """
    게임 리포트 생성 및 업데이트 서비스
    """

    @staticmethod
    @transaction.atomic
    def update_or_create_game_report(report, game):
        """
        특정 게임에 대한 GameReport 업데이트 또는 생성

        Args:
            report: Report 객체
            game: Game 객체

        Returns:
            GameReport 객체
        """
        # GameReport 조회 또는 생성
        game_report, created = GameReport.objects.get_or_create_for_report_and_game(
            report=report,
            game=game,
        )

        # 최신 세션 확인
        latest_session_id = game_report.get_actual_latest_session_id()

        # 이미 최신 상태라면 업데이트 불필요
        if not created and game_report.last_reflected_session_id == latest_session_id:
            return game_report

        # 게임 관련 통계 및 분석 업데이트
        game_report.aggregate_statistics()

        # meta를 재로드하여 최신 통계 데이터 가져오기
        game_report.refresh_from_db(fields=["meta"])

        # meta 데이터가 있으면 LLM 조언 생성
        if game_report.meta:
            GameReportGenerationService._generate_game_report_advice(game_report, game)

        # 최신 세션으로 업데이트
        game_report.last_reflected_session_id = latest_session_id
        game_report.save(update_fields=["last_reflected_session_id", "updated_at"])

        return game_report

    @staticmethod
    def _generate_game_report_advice(game_report, game):
        """
        LLM을 사용하여 게임 리포트 조언 생성

        Args:
            game_report: GameReport 객체 (meta 필드에 통계 데이터 포함)
            game: Game 객체
        """
        # 기존 조언 삭제
        GameReportAdvice.objects.filter(game_report=game_report).delete()

        # meta에서 통계 데이터 가져오기
        statistics = game_report.meta

        # 통계 데이터가 없으면 조언 생성 건너뛰기
        if not statistics or all(v == 0 for v in statistics.values()):
            logger.info(f"No data available for game report {game_report.id}. Skipping advice generation.")
            return

        # 게임별로 적절한 Generator 선택
        generator = None

        if game.code == GameCodeChoice.KIDS_TRAFFIC:
            generator = KidsTrafficGameReportAdviceGenerator()
        elif game.code == GameCodeChoice.BB_STAR:
            generator = BBStarGameReportAdviceGenerator()
        else:
            logger.warning(f"Unknown game code: {game.code}. Skipping advice generation.")
            return

        # LLM을 사용하여 조언 생성
        try:
            advice_list = generator.generate_advice(statistics)

            # 조언을 DB에 저장
            for advice_item in advice_list:
                GameReportAdvice.objects.create(
                    game_report=game_report,
                    game=game,
                    title=advice_item["title"],
                    description=advice_item["description"],
                )

            logger.info(f"Successfully generated {len(advice_list)} advices for game report {game_report.id}")

        except Exception as e:
            # 오류 발생 시 에러 메시지와 함께 조언 저장
            logger.error(f"Failed to generate advice for game report {game_report.id}: {str(e)}")
            GameReportAdvice.objects.create(
                game_report=game_report,
                game=game,
                title="조언 생성 실패",
                description="조언 생성 중 오류가 발생했습니다.",
                error_message=str(e),
            )
