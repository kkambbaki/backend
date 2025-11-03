from django.shortcuts import get_object_or_404
from django.utils import timezone

from games.choices.game_code_choice import GameCodeChoice
from games.choices.game_session_status_choice import GameSessionStatusChoice
from games.models import Game, GameResult, GameSession
from rest_framework import status
from rest_framework.response import Response

from api.v1.games.serializers import BBStarFinishSerializer, BBStarStartSerializer
from common.exceptions.not_found_error import NotFoundError
from common.exceptions.validation_error import ValidationError
from common.permissions.active_user_permission import ActiveUserPermission
from common.views import BaseAPIView


class BBStarStartAPIView(BaseAPIView):
    permission_classes = BaseAPIView.permission_classes + [ActiveUserPermission]

    def post(self, request):
        serializer = BBStarStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        child_id = serializer.validated_data["child_id"]

        try:
            game = Game.objects.by_code(GameCodeChoice.BB_STAR).get()
        except Game.DoesNotExist:
            raise NotFoundError(message="게임( BB_STAR, 뿅뿅 아기별 게임 )이 활성화되어 있지 않습니다.")

        from users.models.child import Child

        child = get_object_or_404(Child, id=child_id)

        session = GameSession.objects.create(
            parent=request.user,
            child=child,
            game=game,
            status=GameSessionStatusChoice.STARTED,
            started_at=timezone.now(),
        )

        return Response(
            {
                "session_id": str(session.id),
                "game_code": game.code,
                "started_at": session.started_at,
                "status": session.status,
            },
            status=status.HTTP_201_CREATED,
        )


class BBStarFinishAPIView(BaseAPIView):
    permission_classes = BaseAPIView.permission_classes + [ActiveUserPermission]

    def post(self, request):
        serializer = BBStarFinishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            session = GameSession.objects.get(id=data["session_id"], parent=request.user)
        except GameSession.DoesNotExist:
            raise NotFoundError(message="세션을 찾을 수 없거나 접근 권한이 없습니다.")

        if session.status == GameSessionStatusChoice.COMPLETED:
            raise ValidationError(message="이미 완료된 세션입니다.")

        session.status = GameSessionStatusChoice.COMPLETED
        session.save(update_fields=["status"])

        result = GameResult.objects.create(
            session=session,
            child=session.child,
            game=session.game,
            score=data["score"],
            wrong_count=data.get("wrong_count", 0),
            reaction_ms_avg=data.get("reaction_ms_avg"),
            success_rate=data.get("success_rate"),
        )

        return Response(
            {
                "session_id": str(session.id),
                "game_code": session.game.code,
                "score": result.score,
                "wrong_count": result.wrong_count,
                "reaction_ms_avg": result.reaction_ms_avg,
                "success_rate": str(result.success_rate) if result.success_rate is not None else None,
            },
            status=status.HTTP_200_OK,
        )
