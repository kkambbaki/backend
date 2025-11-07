from rest_framework import serializers


class GameStartSerializer(serializers.Serializer):
    """게임 시작 공통 Serializer"""

    child_id = serializers.IntegerField(required=True)


class GameStartResponseSerializer(serializers.Serializer):
    """게임 시작 응답 공통 Serializer"""

    session_id = serializers.UUIDField(read_only=True)
    game_code = serializers.CharField(read_only=True)
    started_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)


class GameFinishSerializer(serializers.Serializer):
    """
    게임 종료 공통 Serializer

    meta 필드 구조 예시:
    {
        "early_success_rate": 0.8,        # 초반 성공율 (0.0 ~ 1.0)
        "late_success_rate": 0.6,         # 후반 성공율 (0.0 ~ 1.0)
        "time_limit_exceed_rate": 0.2,    # 제한시간 초과 비율 (0.0 ~ 1.0)
        "round_details": [...]            # 라운드별 상세 데이터 (선택)
    }
    """

    session_id = serializers.UUIDField(required=True)
    score = serializers.IntegerField(required=True)
    wrong_count = serializers.IntegerField(required=False, default=0)
    reaction_ms_sum = serializers.IntegerField(required=False, allow_null=True)
    round_count = serializers.IntegerField(required=False, allow_null=True)
    success_count = serializers.IntegerField(required=False, allow_null=True)
    meta = serializers.JSONField(
        required=False,
        allow_null=True,
        default=dict,
    )


class GameFinishResponseSerializer(serializers.Serializer):
    """게임 종료 응답 공통 Serializer"""

    session_id = serializers.UUIDField(read_only=True)
    game_code = serializers.CharField(read_only=True)
    score = serializers.IntegerField(read_only=True)
    wrong_count = serializers.IntegerField(read_only=True)
    reaction_ms_sum = serializers.IntegerField(read_only=True, allow_null=True)
    round_count = serializers.IntegerField(read_only=True, allow_null=True)
    success_count = serializers.IntegerField(read_only=True, allow_null=True)
