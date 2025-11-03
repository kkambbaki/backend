from django.urls import path

from .views import BBStarFinishAPIView, BBStarStartAPIView

app_name = "games"

urlpatterns = [
    path("bb-star/start/", BBStarStartAPIView.as_view(), name="bb_star_start"),
    path("bb-star/finish/", BBStarFinishAPIView.as_view(), name="bb_star_finish"),
]
