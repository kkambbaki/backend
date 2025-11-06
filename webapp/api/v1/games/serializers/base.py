from rest_framework import serializers


class GameStartSerializer(serializers.Serializer):
    """게임 시작 공통 Serializer"""

    child_id = serializers.IntegerField(required=True)


class GameFinishSerializer(serializers.Serializer):
    """게임 종료 공통 Serializer"""

    session_id = serializers.UUIDField(required=True)
    score = serializers.IntegerField(required=True)
    wrong_count = serializers.IntegerField(required=False, default=0)
    reaction_ms_sum = serializers.IntegerField(required=False, allow_null=True)
    round_count = serializers.IntegerField(required=False, allow_null=True)
    success_count = serializers.IntegerField(required=False, allow_null=True)
