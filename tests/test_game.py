import unittest
import numpy as np

from rps.bot import Bot
from rps.game import Game
from rps.player import Player
import rps.constant as Constant


class GameTest(unittest.TestCase):

    def setUp(self):
        player = Player()
        bot = Bot(epsilon=0.7, learning_rate=0.1, discount_factor=0.5)
        self.game = Game(player=player, bot=bot)

    def test_add_tie(self):
        self.assertEqual(0, self.game.get_nb_of_tie())
        self.game.add_tie()
        self.assertEqual(1, self.game.get_nb_of_tie())

    def test_add_game(self):
        self.assertEqual(0, self.game.get_nb_of_games())
        self.game.add_game()
        self.assertEqual(1, self.game.get_nb_of_games())

    def test_play(self):
        result = self.game.play(player_choice="rock")
        self.assertIn(f'You played rock', result)
        self.assertTrue('I played rock' in result or 'I played paper' in result or 'I played scissors' in result)
        self.assertTrue('tie' in result or 'loose' in result or 'win' in result)

    def test_game_result(self):
        # tie tests
        self.assertEqual("tie", self.game.game_result(player_choice=Constant.ROCK, bot_choice=Constant.ROCK))
        self.assertEqual("tie", self.game.game_result(player_choice=Constant.PAPER, bot_choice=Constant.PAPER))
        self.assertEqual("tie", self.game.game_result(player_choice=Constant.SCISSORS, bot_choice=Constant.SCISSORS))

        # player win tests
        self.assertEqual("win", self.game.game_result(player_choice=Constant.ROCK, bot_choice=Constant.SCISSORS))
        self.assertEqual("win", self.game.game_result(player_choice=Constant.PAPER, bot_choice=Constant.ROCK))
        self.assertEqual("win", self.game.game_result(player_choice=Constant.SCISSORS, bot_choice=Constant.PAPER))

        # player loose tests
        self.assertEqual("loose", self.game.game_result(player_choice=Constant.ROCK, bot_choice=Constant.PAPER))
        self.assertEqual("loose", self.game.game_result(player_choice=Constant.PAPER, bot_choice=Constant.SCISSORS))
        self.assertEqual("loose", self.game.game_result(player_choice=Constant.SCISSORS, bot_choice=Constant.ROCK))

    def test_game_result_history(self):
        # Make player win two times
        self.assertEqual("win", self.game.game_result(player_choice=Constant.ROCK, bot_choice=Constant.SCISSORS))
        self.assertEqual("win", self.game.game_result(player_choice=Constant.PAPER, bot_choice=Constant.ROCK))

        # Make one game tie
        self.assertEqual("tie", self.game.game_result(player_choice=Constant.ROCK, bot_choice=Constant.ROCK))

        # Make player loose one time
        self.assertEqual("loose", self.game.game_result(player_choice=Constant.ROCK, bot_choice=Constant.PAPER))

        # Game results
        self.assertDictEqual(
            {'player_wins': 2, 'bot_wins': 1, 'nb_of_tie': 1, 'nb_of_games': 4,
             'player_percentage_win': 0.5, 'bot_percentage_win': 0.25, 'percentage_of_tie': 0.25},
            self.game.game_result_history()
        )

        # Game Reset to check if result history reset
        self.game.reset()
        self.assertDictEqual(
            {'player_wins': 0, 'bot_wins': 0, 'nb_of_tie': 0, 'nb_of_games': 0,
             'player_percentage_win': 0., 'bot_percentage_win': 0., 'percentage_of_tie': 0.},
            self.game.game_result_history()
        )

    def test_reset(self):
        # add game and tie to tests game reset
        self.game.add_game()
        self.assertEqual(1, self.game.get_nb_of_games())

        self.game.add_tie()
        self.assertEqual(1, self.game.get_nb_of_tie())

        # bot win and q_table to tests game reset
        self.game.bot.add_win()
        self.assertEqual(1, self.game.bot.get_nb_of_wins())
        previous_q_table = self.game.bot.q_values.copy()

        # player win to tests game reset
        self.game.player.add_win()
        self.assertEqual(1, self.game.player.get_nb_of_wins())

        # game tests reset
        self.game.reset()
        self.assertEqual(0, self.game.get_nb_of_games())
        self.assertEqual(0, self.game.get_nb_of_tie())

        # bot reset tests
        self.assertEqual(0, self.game.bot.get_nb_of_wins())
        self.assertFalse(np.array_equal(previous_q_table, self.game.bot.q_values))

        # player reset tests
        self.assertEqual(0, self.game.player.get_nb_of_wins())
