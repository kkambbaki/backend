from drf_spectacular.utils import OpenApiResponse, extend_schema
from reports.authentication import ReportBotAuthentication
from reports.models import Report
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.v1.reports.serializers import ReportDetailSerializer
from common.exceptions.not_found_error import NotFoundError
from common.permissions.active_user_permission import ActiveUserPermission
from common.views import BaseAPIView


@extend_schema(tags=["리포트"])
class ReportDetailAPIView(BaseAPIView):
    authentication_classes = [
        JWTAuthentication,
        ReportBotAuthentication,
    ]
    permission_classes = [ActiveUserPermission]

    @extend_schema(
        operation_id="get_report_detail",
        summary="리포트 상세 조회",
        description="특정 아동에 대한 리포트 상세 정보를 조회합니다.",
        responses={
            200: OpenApiResponse(
                response=ReportDetailSerializer,
                description="리포트 조회 성공",
            ),
            404: OpenApiResponse(description="리포트를 찾을 수 없음"),
        },
    )
    def get(self, request):
        """리포트 상세 조회"""
        # 아동 확인
        user = request.user
        child = user.child

        if not child:
            raise NotFoundError(message="등록된 자녀 정보가 없습니다.")

        # 리포트 조회
        try:
            report = (
                Report.objects.select_related("child", "user")
                .prefetch_related(
                    "game_reports",
                    "game_reports__game",
                    "game_reports__advices",
                    "game_reports__last_reflected_session",
                )
                .get(user=request.user, child=child)
            )
        except Report.DoesNotExist:
            raise NotFoundError(message="리포트를 찾을 수 없습니다.")

        serializer = ReportDetailSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
