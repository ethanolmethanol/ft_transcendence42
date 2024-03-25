from django.urls import path
from .views import GameAPIView, health, index

urlpatterns = [
    path('health/', health, name='health-check'),
    path('', index, name='index'),
    path('games/', GameAPIView.as_view(), name='game_list'),
]