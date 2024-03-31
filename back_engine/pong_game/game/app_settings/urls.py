from django.urls import path
from .views import health, list_rooms, create_room, check_room_exists

urlpatterns = [
    path('health/', health, name='health-check'),
    path('rooms/', list_rooms, name='list_rooms'),
    path('create_room/', create_room, name='create_room'),
    path('check_rooms_exists/<str:room_id>/', check_room_exists, name='check_room_exists'),
]