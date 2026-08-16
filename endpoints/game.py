from flask import Blueprint, request, session
from flask_restx import Api, Resource 
from db_actions.game import get_all, get_game_info

bp = Blueprint("games", __name__)
api = Api(bp, default="games", default_label="games")


class GameAll(Resource):
    def get(self):
        return get_all()

class GameInfo(Resource):
    def get(self, _id):
        return get_game_info(_id)

api.add_resource(GameAll, "/api/games")
api.add_resource(GameInfo, "/api/game/<_id>")