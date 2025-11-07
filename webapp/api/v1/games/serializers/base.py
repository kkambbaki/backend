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
    """게임 종료 공통 Serializer"""

    session_id = serializers.UUIDField(required=True)
    score = serializers.IntegerField(required=True)
    wrong_count = serializers.IntegerField(required=False, default=0)
    reaction_ms_sum = serializers.IntegerField(required=False, allow_null=True)
    round_count = serializers.IntegerField(required=False, allow_null=True)
    success_count = serializers.IntegerField(required=False, allow_null=True)


class GameFinishResponseSerializer(serializers.Serializer):
    """게임 종료 응답 공통 Serializer"""

    session_id = serializers.UUIDField(read_only=True)
    game_code = serializers.CharField(read_only=True)
    score = serializers.IntegerField(read_only=True)
    wrong_count = serializers.IntegerField(read_only=True)
    reaction_ms_sum = serializers.IntegerField(read_only=True, allow_null=True)
    round_count = serializers.IntegerField(read_only=True, allow_null=True)
    success_count = serializers.IntegerField(read_only=True, allow_null=True)
