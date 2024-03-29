from django.urls import path
from .views import health, index, GameAPIView, start_game, update_game, get_game_state

urlpatterns = [
    path('health/', health, name='health-check'),
    path('', index, name='index'),
    path('games/', GameAPIView.as_view(), name='game_list'),
    path('start_game/', start_game, name='start_game'),
    path('update_game/<int:game_id>/', update_game, name='update_game'),
    path('get_game_state/<int:game_id>/', get_game_state, name='get_game_state'),
]