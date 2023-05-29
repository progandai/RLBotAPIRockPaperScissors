import unittest

from rps.player import Player


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.player = Player()

    def test_add_win(self):
        self.assertEqual(0, self.player.get_nb_of_wins())
        self.player.add_win()
        self.assertEqual(1, self.player.get_nb_of_wins())

    def test_reset(self):
        self.player.add_win()
        self.assertEqual(1, self.player.get_nb_of_wins())
        self.player.reset()
        self.assertEqual(0, self.player.get_nb_of_wins())
