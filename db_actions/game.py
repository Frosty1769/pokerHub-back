import uuid
from flask import jsonify, session
from db import db
from model.model import Games

def get_all():
    _games: Games = db.session.query(Games).all()

    res = []
    for game in _games:
        print(_games)
        res.append({"id": game.id_public, "name": game.name, "deposit": game.deposit, "max_players": game.max_players})
    return jsonify({"data": res,"status": "ok"})

def get_game_info(id):
    _game = db.session.query(Games).filter(Games.id_public == id).first()
    res = {"id": _game.id_public, "description": _game.description, "player_count": 4, "name": _game.name, "deposit": _game.deposit, "player_maxcount": _game.max_players}
    return jsonify({"data": res,"status": "ok"})