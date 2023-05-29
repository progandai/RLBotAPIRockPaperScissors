from flask import Flask, Blueprint
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from api.game import game_namespace

#import logging
#logger = logging.getLogger('gunicorn.error')


def initialize_app():
    """
    Initialize Flask application with Flask-RestPlus
    :return flask_app: instance of Flask() class
    """
    # Init Flask app
    flask_app = Flask(__name__)
    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1/rps')
    app = Api(
        app=blueprint,
        version="1.0.0",
        title="RPS MicroService"
    )
    # Add namespaces
    app.add_namespace(game_namespace)
    # Add blueprint
    flask_app.register_blueprint(blueprint)
    #flask_app.logger.handlers = logger.handlers
    #flask_app.logger.setLevel(logger.level)
    return flask_app
