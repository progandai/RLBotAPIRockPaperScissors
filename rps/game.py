import rps.constant as Constant


class Game:

    def __init__(self, player, bot):
        self.nb_of_games = 0
        self.nb_of_tie = 0
        self.player = player
        self.bot = bot

    def get_nb_of_tie(self):
        return self.nb_of_tie

    def add_tie(self):
        self.nb_of_tie += 1

    def get_nb_of_games(self):
        return self.nb_of_games

    def add_game(self):
        self.nb_of_games += 1

    def play(self, player_choice):
        bot_choice_index = self.bot.get_bot_next_action(player_choice)
        bot_choice = self.bot.get_rps_val(bot_choice_index)
        self.bot.train_bot(player_choice, bot_choice_index)
        game_result = self.game_result(player_choice, bot_choice)
        if game_result == Constant.GAME_TIE:
            return f"You played {player_choice}, I played {bot_choice}, it's a {game_result}!"
        return f"You played {player_choice}, I played {bot_choice}, you {game_result}!"

    def game_result(self, player_choice, bot_choice):
        self.add_game()
        if player_choice == bot_choice:
            self.add_tie()
            return Constant.GAME_TIE
        elif player_choice == Constant.ROCK and bot_choice == Constant.SCISSORS:
            self.player.add_win()
            return Constant.GAME_WIN
        elif player_choice == Constant.PAPER and bot_choice == Constant.ROCK:
            self.player.add_win()
            return Constant.GAME_WIN
        elif player_choice == Constant.SCISSORS and bot_choice == Constant.PAPER:
            self.player.add_win()
            return Constant.GAME_WIN
        else:
            self.bot.add_win()
            return Constant.GAME_LOOSE

    def game_result_history(self):
        return {
            "player_wins": self.player.get_nb_of_wins(),
            "bot_wins": self.bot.get_nb_of_wins(),
            "nb_of_tie": self.nb_of_tie,
            "nb_of_games": self.get_nb_of_games(),
            "player_percentage_win": round(self.player.get_nb_of_wins() / self.get_nb_of_games(), 2) if self.get_nb_of_games() > 0 else 0,
            "bot_percentage_win": round(self.bot.get_nb_of_wins() / self.get_nb_of_games(), 2) if self.get_nb_of_games() > 0 else 0,
            "percentage_of_tie": round(self.get_nb_of_tie() / self.get_nb_of_games(), 2) if self.get_nb_of_games() > 0 else 0
        }

    def reset(self):
        self.nb_of_games = 0
        self.nb_of_tie = 0
        self.player.reset()
        self.bot.reset()
