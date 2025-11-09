from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from drf_spectacular.utils import OpenApiResponse, extend_schema
from games.choices.game_code_choice import GameCodeChoice
from games.choices.game_session_status_choice import GameSessionStatusChoice
from games.models import Game, GameResult, GameSession
from rest_framework import status
from rest_framework.response import Response

from api.v1.games.serializers import (
    BBStarFinishSerializer,
    BBStarStartSerializer,
    GameFinishResponseSerializer,
    GameStartResponseSerializer,
)
from common.exceptions.not_found_error import NotFoundError
from common.exceptions.validation_error import ValidationError
from common.permissions.active_user_permission import ActiveUserPermission
from common.views import BaseAPIView
from users.models.child import Child


@extend_schema(tags=["게임 - 뿅뿅 아기별"])
class BBStarStartAPIView(BaseAPIView):
    permission_classes = [ActiveUserPermission]

    @extend_schema(
        operation_id="start_bb_star_game",
        summary="뿅뿅 아기별 게임 시작",
        description="아이를 위한 뿅뿅 아기별 게임 세션을 시작합니다.",
        request=BBStarStartSerializer,
        responses={
            201: OpenApiResponse(
                response=GameStartResponseSerializer,
                description="게임 세션 시작 성공",
            ),
            404: OpenApiResponse(description="게임 또는 아이를 찾을 수 없음"),
        },
    )
    def post(self, request):
        serializer = BBStarStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        child_id = serializer.validated_data["child_id"]

        try:
            game = get_object_or_404(Game.objects.by_code(GameCodeChoice.BB_STAR))
        except Http404:
            raise NotFoundError(message="게임( BB_STAR, 뿅뿅 아기별 게임 )이 활성화되어 있지 않습니다.")
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


@extend_schema(tags=["게임 - 뿅뿅 아기별"])
class BBStarFinishAPIView(BaseAPIView):
    permission_classes = [ActiveUserPermission]

    @extend_schema(
        operation_id="finish_bb_star_game",
        summary="뿅뿅 아기별 게임 종료",
        description="뿅뿅 아기별 게임 세션을 종료하고 결과를 저장합니다.",
        request=BBStarFinishSerializer,
        responses={
            200: OpenApiResponse(
                response=GameFinishResponseSerializer,
                description="게임 세션 종료 성공",
            ),
            404: OpenApiResponse(description="세션을 찾을 수 없거나 접근 권한이 없음"),
            400: OpenApiResponse(description="이미 완료된 세션"),
        },
    )
    def post(self, request):
        serializer = BBStarFinishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        with transaction.atomic():
            try:
                session = (
                    GameSession.objects.select_related("child", "game")
                    .select_for_update()
                    .get(id=data["session_id"], parent=request.user)
                )
            except GameSession.DoesNotExist:
                raise NotFoundError(message="세션을 찾을 수 없거나 접근 권한이 없습니다.")

            if session.status == GameSessionStatusChoice.COMPLETED:
                raise ValidationError(message="이미 완료된 세션입니다.")

            session.status = GameSessionStatusChoice.COMPLETED
            session.ended_at = timezone.now()
            session.save(update_fields=["status", "ended_at"])

            result = GameResult.objects.create(
                session=session,
                child=session.child,
                game=session.game,
                score=data["score"],
                wrong_count=data.get("wrong_count", 0),
                reaction_ms_sum=data.get("reaction_ms_sum"),
                round_count=data.get("round_count"),
                success_count=data.get("success_count"),
                meta=data.get("meta", {}),
            )

        return Response(
            {
                "session_id": str(session.id),
                "game_code": session.game.code,
                "score": result.score,
                "wrong_count": result.wrong_count,
                "reaction_ms_sum": result.reaction_ms_sum,
                "round_count": result.round_count,
                "success_count": result.success_count,
            },
            status=status.HTTP_200_OK,
        )
