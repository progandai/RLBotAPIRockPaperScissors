import numpy as np

import rps.constant as Constant


class Bot:

    def __init__(self, epsilon, learning_rate, discount_factor):
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.env_dim = 3
        self.rewards = np.array([
            Constant.ROCK_REWARD_LIST,
            Constant.PAPER_REWARD_LIST,
            Constant.SCISSORS_REWARD_LIST
        ])
        self.q_values = np.random.uniform(low=0, high=1, size=(self.env_dim, self.env_dim))
        self.RPS_INDEX = {
            Constant.ROCK: Constant.ROCK_INDEX,
            Constant.PAPER: Constant.PAPER_INDEX,
            Constant.SCISSORS: Constant.SCISSORS_INDEX
        }
        self.RPS_VAL = {
            Constant.ROCK_INDEX: Constant.ROCK,
            Constant.PAPER_INDEX: Constant.PAPER,
            Constant.SCISSORS_INDEX: Constant.SCISSORS
        }
        self.nb_of_wins = 0

    def get_nb_of_wins(self):
        return self.nb_of_wins

    def add_win(self):
        self.nb_of_wins += 1

    def get_rps_index(self, choice):
        return self.RPS_INDEX[choice]

    def get_rps_val(self, choice_index):
        return self.RPS_VAL[choice_index]

    # define an epsilon greedy algorithm that will choose which action to take next (i.e., where to move next)
    def get_bot_next_action(self, player_choice):
        # if a randomly chosen value between 0 and 1 is less than epsilon,
        # then choose the most promising value from the Q-table for this state.
        player_choice_index = self.get_rps_index(player_choice)
        if np.random.random() < self.epsilon:
            return np.argmax(self.q_values[player_choice_index])
        else:  # choose a random action
            return np.random.randint(3)

    def get_reward(self, player_choice_index, bot_choice_index):
        return self.rewards[player_choice_index, bot_choice_index]

    def train_bot(self, player_choice, bot_choice_index):
        player_choice_index = self.get_rps_index(player_choice)
        reward = self.get_reward(player_choice_index, bot_choice_index)
        old_value = self.q_values[player_choice_index, bot_choice_index]
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * \
                    (reward + self.discount_factor * np.max(self.q_values[player_choice_index]))
        self.q_values[player_choice_index, bot_choice_index] = new_value

    def reset(self):
        self.nb_of_wins = 0
        self.q_values = np.random.uniform(low=0, high=1, size=(self.env_dim, self.env_dim))
