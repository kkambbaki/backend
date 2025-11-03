from rest_framework import serializers


class BBStarStartSerializer(serializers.Serializer):
    child_id = serializers.IntegerField(required=True)


class BBStarFinishSerializer(serializers.Serializer):
    session_id = serializers.UUIDField(required=True)
    score = serializers.IntegerField(required=True)
    wrong_count = serializers.IntegerField(required=False, default=0)
    reaction_ms_avg = serializers.IntegerField(required=False, allow_null=True)
    success_rate = serializers.DecimalField(max_digits=5, decimal_places=2, required=False, allow_null=True)
