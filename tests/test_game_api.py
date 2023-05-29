import json
import unittest

from api.app import initialize_app


class GameApiTest(unittest.TestCase):

    def setUp(self):
        self.app = initialize_app()
        self.client = self.app.test_client()
        self.game_api_url = '/api/v1/rps/game'

    def test_play(self):
        # Player Given
        payload = json.dumps({
            "myHand": "rock"
        })

        # When
        response = self.client.post(f'{self.game_api_url}/play', headers={"Content-Type": "application/json"},
                                    data=payload)

        # Then
        self.assertEqual(str, type(response.json['result']))
        result = response.json['result']
        self.assertIn('You played rock', result)
        self.assertTrue('I played rock' in result or 'I played paper' in result or 'I played scissors' in result)
        self.assertTrue('tie' in result or 'loose' in result or 'win' in result)
        self.assertEqual(200, response.status_code)

    def test_results(self):
        # When
        response = self.client.get(f'{self.game_api_url}/results', headers={"Content-Type": "application/json"})

        # Then
        results = response.json
        self.assertIn('player_wins', results)
        self.assertEqual(0, results['player_wins'])

        self.assertIn('bot_wins', results)
        self.assertEqual(0, results['bot_wins'])

        self.assertIn('nb_of_tie', results)
        self.assertEqual(0, results['nb_of_tie'])

        self.assertIn('nb_of_games', results)
        self.assertEqual(0, results['nb_of_games'])

        self.assertIn('player_percentage_win', results)
        self.assertEqual(0., results['player_percentage_win'])

        self.assertIn('player_percentage_win', results)
        self.assertEqual(0., results['player_percentage_win'])

        self.assertIn('percentage_of_tie', results)
        self.assertEqual(0., results['percentage_of_tie'])

        self.assertEqual(200, response.status_code)

    def test_reset(self):
        # When
        response = self.client.get(f'{self.game_api_url}/reset', headers={"Content-Type": "application/json"})

        # Then
        self.assertEqual(str, type(response.json['message']))
        self.assertEqual('New game started...', response.json['message'])
        self.assertEqual(200, response.status_code)
