from django.db import models
from django.db.models import Avg, Count, Sum
from django.utils.translation import gettext_lazy as _

from games.choices import GameCodeChoice
from games.models import GameResult

from common.models import BaseModel, BaseModelManager


class GameReportManager(BaseModelManager):
    def by_report(self, report):
        return self.filter(report=report)

    def by_game(self, game):
        return self.filter(game=game)

    def get_or_create_for_report_and_game(self, report, game):
        """리포트와 게임에 대한 게임 리포트 조회 또는 생성"""
        game_report, created = self.get_or_create(
            report=report,
            game=game,
        )
        return game_report, created


class GameReport(BaseModel):
    """
    게임별 리포트 모델
    특정 리포트 내의 각 게임에 대한 결과 및 분석
    """

    class Meta:
        db_table = "game_reports"
        verbose_name = _("게임 리포트")
        verbose_name_plural = _("게임 리포트")
        constraints = [
            models.UniqueConstraint(
                fields=["report", "game"],
                name="unique_report_game",
            ),
        ]
        ordering = ["-updated_at"]

    objects = GameReportManager()

    report = models.ForeignKey(
        "reports.Report",
        on_delete=models.CASCADE,
        related_name="game_reports",
        null=False,
        blank=False,
        verbose_name=_("리포트"),
    )
    game = models.ForeignKey(
        "games.Game",
        on_delete=models.CASCADE,
        related_name="game_reports",
        null=False,
        blank=False,
        verbose_name=_("게임"),
    )
    last_reflected_session = models.ForeignKey(
        "games.GameSession",
        on_delete=models.SET_NULL,
        related_name="reflected_in_game_reports",
        null=True,
        blank=True,
        verbose_name=_("마지막 반영 세션"),
        help_text="가장 최근 반영된 게임 세션",
    )
    meta = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("메타 정보"),
        help_text="게임 결과를 추합한 게임과 관련된 추가 메타 정보",
    )

    def __str__(self):
        return f"{self.report} - {self.game.name}"

    def get_actual_latest_session_id(self):
        """
        해당 게임의 최신 세션 조회

        Returns:
            GameSession or None: 최신 세션 객체 또는 None
        """

        latest_result = (
            GameResult.objects.filter(
                child=self.report.child,
                game=self.game,
            )
            .select_related("session")
            .order_by("-updated_at")
            .first()
        )

        return latest_result.session.id if latest_result else None

    def is_up_to_date(self):
        """
        현재 게임 리포트가 최신 GameSession을 반영하고 있는지 확인

        Returns:
            bool: 최신 세션을 반영하고 있으면 True, 아니면 False
        """
        latest_session_id = self.get_actual_latest_session_id()

        if not latest_session_id:
            return True

        return self.last_reflected_session_id == latest_session_id

    def get_game_results(self):
        """
        해당 게임 리포트에 해당하는 모든 게임 결과 조회

        Returns:
            QuerySet: GameResult 쿼리셋
        """
        return GameResult.objects.filter(
            child=self.report.child,
            game=self.game,
        ).order_by("-created_at")

    def aggregate_statistics(self):
        """
        게임 결과를 집계하여 통계 데이터 생성 및 meta 필드에 저장

        Returns:
            dict: 게임별 통계 데이터 (meta 필드에도 저장됨)
        """
        game_results = self.get_game_results()

        if not game_results.exists():
            return None

        # 게임 코드별로 다른 통계 계산
        statistics = None
        if self.game.code == GameCodeChoice.KIDS_TRAFFIC:
            statistics = self._aggregate_kids_traffic_statistics(game_results)
        elif self.game.code == GameCodeChoice.BB_STAR:
            statistics = self._aggregate_bb_star_statistics(game_results)

        # 통계 데이터를 meta 필드에 저장
        if statistics:
            self.meta = statistics
            self.save(update_fields=["meta", "updated_at"])

        return statistics

    def _aggregate_kids_traffic_statistics(self, game_results):
        """
        꼬마 교통지킴이 게임 통계 집계

        Args:
            game_results: GameResult 쿼리셋

        Returns:
            dict: 통계 데이터
                - error_rate: 실수율 (%)
                - reaction_time: 평균 반응속도 (초)
                - avg_focus_time: 평균 집중시간 (분)
                - session_count: 세션 수
        """
        stats = game_results.aggregate(
            total_rounds=Sum("round_count"),
            total_wrong=Sum("wrong_count"),
            avg_reaction_ms=Avg("reaction_ms_sum"),
            session_count=Count("id"),
        )

        total_rounds = stats["total_rounds"] or 0
        total_wrong = stats["total_wrong"] or 0
        avg_reaction_ms = stats["avg_reaction_ms"] or 0
        session_count = stats["session_count"] or 0

        # 실수율 계산 (오답 / 총 라운드 * 100)
        error_rate = (total_wrong / total_rounds * 100) if total_rounds > 0 else 0

        # 반응속도를 초 단위로 변환 (평균 반응 시간 / 라운드 수)
        avg_reaction_time_per_round = avg_reaction_ms / total_rounds if total_rounds > 0 else 0
        reaction_time = avg_reaction_time_per_round / 1000  # ms -> seconds

        # 평균 집중시간 (분) - 각 세션의 메타 데이터에서 추출
        focus_times = []
        for result in game_results:
            if result.meta and "focus_time_minutes" in result.meta:
                focus_times.append(result.meta["focus_time_minutes"])

        avg_focus_time = sum(focus_times) / len(focus_times) if focus_times else 10  # 기본값 10분

        return {
            "error_rate": round(error_rate, 2),
            "reaction_time": round(reaction_time, 2),
            "avg_focus_time": round(avg_focus_time, 2),
            "session_count": session_count,
        }

    def _aggregate_bb_star_statistics(self, game_results):
        """
        뿅뿅 아기별 게임 통계 집계

        Args:
            game_results: GameResult 쿼리셋

        Returns:
            dict: 통계 데이터
                - early_success_rate: 초반 성공률 (%)
                - late_success_rate: 후반 성공률 (%)
                - error_rate: 오답률 (%)
                - timeout_rate: 제한시간 초과비율 (%)
        """
        total_early_rounds = 0
        total_early_success = 0
        total_late_rounds = 0
        total_late_success = 0
        total_rounds = 0
        total_wrong = 0
        total_timeout = 0

        for result in game_results:
            if not result.meta:
                continue

            # 메타 데이터에서 라운드별 정보 추출
            rounds_data = result.meta.get("rounds", [])

            for idx, round_data in enumerate(rounds_data):
                total_rounds += 1

                # 초반/후반 구분 (전반부 50%는 초반, 후반부 50%는 후반)
                is_early = idx < len(rounds_data) / 2

                if is_early:
                    total_early_rounds += 1
                    if round_data.get("success", False):
                        total_early_success += 1
                else:
                    total_late_rounds += 1
                    if round_data.get("success", False):
                        total_late_success += 1

                # 오답 및 타임아웃 카운트
                if not round_data.get("success", False):
                    total_wrong += 1

                if round_data.get("timeout", False):
                    total_timeout += 1

        # 성공률 계산
        early_success_rate = (total_early_success / total_early_rounds * 100) if total_early_rounds > 0 else 0
        late_success_rate = (total_late_success / total_late_rounds * 100) if total_late_rounds > 0 else 0
        error_rate = (total_wrong / total_rounds * 100) if total_rounds > 0 else 0
        timeout_rate = (total_timeout / total_rounds * 100) if total_rounds > 0 else 0

        return {
            "early_success_rate": round(early_success_rate, 2),
            "late_success_rate": round(late_success_rate, 2),
            "error_rate": round(error_rate, 2),
            "timeout_rate": round(timeout_rate, 2),
        }
