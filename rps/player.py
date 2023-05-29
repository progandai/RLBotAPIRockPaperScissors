class Player:

    def __init__(self):
        self.nb_of_wins = 0

    def get_nb_of_wins(self):
        return self.nb_of_wins

    def add_win(self):
        self.nb_of_wins += 1

    def reset(self):
        self.nb_of_wins = 0
