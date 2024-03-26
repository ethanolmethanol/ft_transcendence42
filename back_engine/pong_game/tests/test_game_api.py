from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Game

class GameAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.game = Game.objects.create(
            ball_position={'x': 0, 'y': 0}, 
            ball_velocity={'x': 1, 'y': 1}, 
            paddle_positions={'left': 0, 'right': 0}
        )
    
    def test_game_initialization(self):
        response = self.client.get('/api/game/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {
            'message': 'Game state', 
            'ball_position': {'x': 0, 'y': 0}, 
            'paddle_positions': {'left': 0, 'right': 0}
        })
    
    def test_game_update(self):
        data = {
            'ball_position': {'x': 1, 'y': 1}, 
            'ball_velocity': {'x': 2, 'y': 2}, 
            'paddle_positions': {'left': 1, 'right': 1}
        }
        response = self.client.post('/api/game/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content), 
            {'message': 'Game state updated'}
        )