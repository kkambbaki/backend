from games.models import Game
from rest_framework import status
from rest_framework.response import Response

from api.v1.games.serializers import GameListSerializer
from common.permissions.active_user_permission import ActiveUserPermission
from common.views import BaseAPIView


class GameListAPIView(BaseAPIView):
    permission_classes = [ActiveUserPermission]

    def get(self, request):
        """
        활성화된 게임 목록 조회
        """
        games = Game.objects.active().order_by("id")
        serializer = GameListSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
