from tests.base_test_case import BaseTestCase
from app.models import Game


class TestMainRoute(BaseTestCase):

    def test_start_game(self):
        response = self.client.get('/category_game/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/game/2')
        game = Game.query.first()
        self.assertIsNotNone(game)
        self.assertEqual(len(game.questions), 1)