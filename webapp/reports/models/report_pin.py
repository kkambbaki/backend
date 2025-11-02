from django.db import models

from common.models import BaseModel


class ReportPin(BaseModel):
    """
    Report Pin model
    """

    class Meta:
        db_table = "report_pins"
        verbose_name = "Report Pin"
        verbose_name_plural = "Report Pins"

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="report_pins",
        verbose_name="User",
    )

    pin_hash = models.CharField(
        max_length=256,
        verbose_name="Pin Hash",
    )

    enabled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Enabled At",
    )
