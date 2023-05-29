import unittest
import numpy as np

from rps.bot import Bot
import rps.constant as Constant


class BotTest(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(epsilon=0.7, learning_rate=0.1, discount_factor=0.5)

    def test_add_win(self):
        self.assertEqual(0, self.bot.get_nb_of_wins())
        self.bot.add_win()
        self.assertEqual(1, self.bot.get_nb_of_wins())

    def test_get_rps_index(self):
        self.assertEqual(0, self.bot.get_rps_index("rock"))
        self.assertEqual(1, self.bot.get_rps_index("paper")),
        self.assertEqual(2, self.bot.get_rps_index("scissors"))

    def test_get_rps_val(self):
        self.assertEqual("rock", self.bot.get_rps_val(0))
        self.assertEqual("paper", self.bot.get_rps_val(1))
        self.assertEqual("scissors", self.bot.get_rps_val(2))

    def test_get_bot_next_action(self):
        self.assertIn(self.bot.get_bot_next_action(player_choice="rock"), np.array([0, 1, 2]))

    def test_get_reward(self):
        self.assertEqual(-1, self.bot.get_reward(player_choice_index=0, bot_choice_index=0))
        self.assertEqual(1, self.bot.get_reward(player_choice_index=1, bot_choice_index=2))
        self.assertEqual(-2, self.bot.get_reward(player_choice_index=2, bot_choice_index=1))

    def test_train_bot(self):
        previous_q_table = self.bot.q_values.copy()
        # Player choose rock and Bot choose paper. Bot win. q_table at position (0,1) must have increase
        self.bot.train_bot(player_choice=Constant.ROCK, bot_choice_index=Constant.PAPER_INDEX)
        self.assertFalse(np.array_equal(previous_q_table, self.bot.q_values))
        self.assertLess(previous_q_table[Constant.ROCK_INDEX][Constant.PAPER_INDEX],
                        self.bot.q_values[Constant.ROCK_INDEX][Constant.PAPER_INDEX])

        previous_q_table = self.bot.q_values.copy()
        # Player choose scissors and Bot choose paper. Player win. q_table at position (2,1) must have decrease
        self.bot.train_bot(player_choice=Constant.SCISSORS, bot_choice_index=Constant.PAPER_INDEX)
        self.assertFalse(np.array_equal(previous_q_table, self.bot.q_values))
        self.assertGreater(previous_q_table[Constant.SCISSORS_INDEX][Constant.PAPER_INDEX],
                           self.bot.q_values[Constant.SCISSORS_INDEX][Constant.PAPER_INDEX])

    def test_reset(self):
        self.bot.add_win()
        self.assertEqual(1, self.bot.get_nb_of_wins())
        previous_q_table = self.bot.q_values.copy()

        self.bot.reset()
        self.assertEqual(0, self.bot.get_nb_of_wins())
        self.assertFalse(np.array_equal(previous_q_table, self.bot.q_values))
