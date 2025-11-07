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

    프론트에서 보내는 정보:
    1. meta 외 필드 (전체 게임 집계 정보):
       - session_id, score, wrong_count, reaction_ms_sum, round_count, success_count

    2. meta 필드 (라운드별 상세 데이터):
       - round_details: 각 라운드의 상세 정보

    meta 필드 구조 예시 (각 라운드별 상세 정보):
    {
        "round_details": [
            {
                "round_number": 1,
                "score": 10,                    # 해당 라운드 점수
                "wrong_count": 1,               # 해당 라운드 틀린 개수
                "reaction_time_ms_sum": 1500,   # 해당 라운드 반응시간 합계
                "is_success": True,             # 해당 라운드 성공 여부
                "time_limit_exceeded": False    # 제한시간 초과 여부
            },
            {
                "round_number": 2,
                "score": 5,
                "wrong_count": 2,
                "reaction_time_ms_sum": 2000,
                "is_success": False,
                "time_limit_exceeded": True
            },
            ...
        ]
    }

    """

    session_id = serializers.UUIDField(
        required=True,
        help_text="게임 세션 식별자 (UUID)",
    )
    score = serializers.IntegerField(
        required=True,
        help_text="게임 전체 총 점수",
    )
    wrong_count = serializers.IntegerField(
        required=False,
        default=0,
        help_text="게임 전체 틀린 개수",
    )
    reaction_ms_sum = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="게임 전체 반응시간 합계 (밀리초)",
    )
    round_count = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="게임 전체 라운드 수",
    )
    success_count = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="게임 전체 성공한 라운드 수",
    )
    meta = serializers.JSONField(
        required=False,
        allow_null=True,
        default=dict,
        help_text=(
            "라운드별 상세 데이터. 구조: "
            "{'round_details': [{'round_number': 1, 'score': 10, 'wrong_count': 1, "
            "'reaction_time_ms_sum': 1500, 'is_success': True, 'time_limit_exceeded': False}, ...]}"
        ),
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
