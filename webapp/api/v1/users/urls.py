from django.urls import include, path

from .views import EmailUpdateAPIView

urlpatterns = [
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("email/", EmailUpdateAPIView.as_view(), name="email-update"),
]
