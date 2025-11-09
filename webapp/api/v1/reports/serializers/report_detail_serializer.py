from reports.models import Report
from rest_framework import serializers

from api.v1.users.serializers import ChildSerializer

from .game_report_detail_serializer import GameReportDetailSerializer

# TODO: Report 정보가 제대로 GameResult의 meta에 따라 잘 만들어지는지 확인하고 내용 수정하기


class ReportDetailSerializer(serializers.ModelSerializer):
    """리포트 상세 정보 Serializer"""

    child = ChildSerializer(
        read_only=True,
    )
    game_reports = GameReportDetailSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "child",
            "concentration_score",
            "game_reports",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
