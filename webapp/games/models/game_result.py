from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from psqlextra.models import PostgresModel

from common.models import BaseModelManager

User = get_user_model()


class GameResultManager(BaseModelManager):
    def by_child(self, child):
        return self.filter(child=child)

    def by_game(self, game):
        return self.filter(game=game)


class GameResult(PostgresModel):
    """
    게임 결과 모델
    완료된 게임 세션의 최종 결과를 저장
    """

    class Meta:
        db_table = "game_results"
        verbose_name = _("게임 결과")
        verbose_name_plural = _("게임 결과")
        constraints = [
            models.UniqueConstraint(fields=["session"], name="unique_session_result"),
        ]
        ordering = ["-created_at"]

    objects = GameResultManager()

    session = models.OneToOneField(
        "games.GameSession",
        on_delete=models.CASCADE,
        related_name="result",
        null=False,
        blank=False,
        db_column="session_id",
        verbose_name=_("게임 세션"),
    )
    child = models.ForeignKey(
        "users.Child",
        on_delete=models.CASCADE,
        related_name="game_results",
        null=False,
        blank=False,
        verbose_name=_("아동"),
    )
    game = models.ForeignKey(
        "games.Game",
        on_delete=models.CASCADE,
        related_name="game_results",
        null=False,
        blank=False,
        verbose_name=_("게임"),
    )
    score = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_("총점"),
    )
    wrong_count = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        verbose_name=_("오답 수"),
    )
    reaction_ms_avg = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_("평균 반응(ms)"),
        help_text="평균 반응 시간",
    )
    success_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("100.00"))],
        verbose_name=_("성공률(%)"),
        help_text="성공률 (0.00 ~ 100.00)",
    )

    def __str__(self):
        return f"{self.child.name} - {self.game.name} (점수: {self.score})"
