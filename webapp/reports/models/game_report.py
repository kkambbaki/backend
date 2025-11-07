from django.db import models
from django.utils.translation import gettext_lazy as _

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

    def latest_session(self):
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

        return latest_result.session if latest_result else None

    def is_up_to_date(self):
        """
        현재 게임 리포트가 최신 GameSession을 반영하고 있는지 확인

        Returns:
            bool: 최신 세션을 반영하고 있으면 True, 아니면 False
        """
        latest_session = self.latest_session()

        if not latest_session:  # 게임 결과가 없으면 up-to-date로 간주
            return True

        # 최신 결과의 세션과 현재 반영된 세션이 같은지 확인
        return self.last_reflected_session_id == latest_session.id
