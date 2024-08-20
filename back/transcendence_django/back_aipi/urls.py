from django.urls import path

from .views import AipiView

urlpatterns = [
    path("spawn/", AipiView.as_view(), name="spawn"),
]
