# import pytest
# import json
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
# from game.models import PongRoom

# @pytest.mark.soft
# @pytest.mark.rooms
# @pytest.mark.django_db
# def test_create_room_success(api_client):
#     url = reverse('create_room')
#     print(url)
#     data = {'room_id': 'testroom1', 'max_players': 4}
#     response = api_client.post(url, data, format='json', follow=True)
#     print(response.content)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert PongRoom.objects.filter(room_id='testroom1').exists()
#     assert response.json['message'] == f"Room testroom1 created successfully."

# @pytest.mark.soft
# @pytest.mark.rooms
# @pytest.mark.django_db
# def test_create_room_failure_existing_room(api_client):
#     PongRoom.objects.create(room_id='testroom2', max_players=4)
#     url = reverse('create_room', follow=True)
#     data = {'room_id': 'testroom2', 'max_players': 4}
#     response = api_client.post(url, data, format='json')
#     assert response.status_code == status.HTTP_400_BAD_REQUEST

# @pytest.mark.soft
# @pytest.mark.rooms
# @pytest.mark.django_db
# def test_check_room_exists(api_client):
#     room_id = 'testroom3'
#     PongRoom.objects.create(room_id=room_id, max_players=4)
#     url = reverse('check_room_exists', kwargs={'room_id': room_id}, follow=True)
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json['message'] == 'Room exists.'

# @pytest.mark.soft
# @pytest.mark.rooms
# @pytest.mark.django_db
# def test_list_rooms(api_client):
#     PongRoom.objects.create(room_id='testroom4', max_players=4)
#     PongRoom.objects.create(room_id='testroom5', max_players=2)

#     url = reverse('list_rooms')
#     response = api_client.get(url, follow=True)
#     assert response.status_code == status.HTTP_200_OK
#     response_data = response.json()
#     assert len(response_data) == 2
