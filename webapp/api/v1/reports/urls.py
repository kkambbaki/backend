from django.urls import path

from .views import set_report_pin_api_view

urlpatterns = [
    path("set-report-pin/", set_report_pin_api_view.SetReportPinAPIView.as_view(), name="set-report-pin"),
]
