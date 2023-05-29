from flask_restx import Namespace, Resource, fields

from rps.bot import Bot
from rps.player import Player
from rps.game import Game

game_namespace = Namespace("game", description="RPS GAME API")

EPSILON = 0.7
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.5

bot = Bot(epsilon=EPSILON, learning_rate=LEARNING_RATE, discount_factor=DISCOUNT_FACTOR)
player = Player()
game = Game(player, bot)

play_parser = game_namespace.parser()
play_parser.add_argument("myHand", type=str, required=True, help="myHand which represents the player choice",
                         location="json", choices=("rock", "paper", "scissors"))

play_res = game_namespace.model(
    "PlayResult", {"result": fields.String(required=True, description="Play result...")}
)

result_res = game_namespace.model(
    "Results", {
        "player_wins": fields.Integer(required=True, description="Number of player wins."),
        "bot_wins": fields.Integer(required=True, description="Number of bot wins."),
        "nb_of_tie": fields.Integer(required=True, description="Number of tie."),
        "nb_of_games": fields.Integer(required=True, description="Number of games played."),
        "player_percentage_win": fields.Float(required=True, description="Player percentage of win."),
        "bot_percentage_win": fields.Float(required=True, description="Bot percentage of win."),
        "percentage_of_tie": fields.Float(required=True, description="Percentage of tie."),
    }
)

reset_res = game_namespace.model(
    "Reset", {"message": fields.String(required=True, description="Reset message")}
)


@game_namespace.route('/play')
class Play(Resource):

    @game_namespace.doc(description="Play API. Player send his choice and the bot try to beat him. "
                                    "The more the user plays, the more the bot is learning."
                                    "The user has 3 choices: rock, paper or scissors.", parser=play_parser)
    @game_namespace.marshal_with(play_res)
    def post(self):
        args = play_parser.parse_args()
        player_choice = args['myHand']
        result = game.play(player_choice)
        return {
            "result": result
        }


@game_namespace.route('/results')
class Results(Resource):

    @game_namespace.doc(description="Return the results of the past games between the user and the bot.")
    @game_namespace.marshal_with(result_res)
    def get(self):
        return game.game_result_history()


@game_namespace.route('/reset')
class Reset(Resource):

    @game_namespace.doc(description="Reset and delete all informations about the previous games.")
    @game_namespace.marshal_with(reset_res)
    def get(self):
        game.reset()
        return {
            "message": "New game started..."
        }
