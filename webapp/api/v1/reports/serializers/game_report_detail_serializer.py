from reports.models import GameReport
from rest_framework import serializers

from .game_report_advice_serializer import GameReportAdviceSerializer


class GameReportDetailSerializer(serializers.ModelSerializer):
    """게임 리포트 Serializer"""

    game_name = serializers.CharField(
        source="game.name",
        read_only=True,
    )
    game_code = serializers.CharField(
        source="game.code",
        read_only=True,
    )
    last_reflected_session_id = serializers.UUIDField(
        source="last_reflected_session.id",
        read_only=True,
        allow_null=True,
    )
    is_up_to_date = serializers.SerializerMethodField()
    advices = GameReportAdviceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = GameReport
        fields = [
            "id",
            "game_name",
            "game_code",
            "last_reflected_session_id",
            "is_up_to_date",
            "advices",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_is_up_to_date(self, obj):
        """게임 리포트가 최신 상태인지 확인"""
        return obj.is_up_to_date()
