import uuid
from flask import jsonify, session
from db import db
from model.model import Users

from model.user import User
from typing import Optional

def get_user_by_telegram_id(telegram_id: str) -> Optional[User]:
    return User.query.filter_by(telegram_id=telegram_id).first()

def create_or_update_user(telegram_user: dict) -> User:
    telegram_id = str(telegram_user['id'])
    user = get_user_by_telegram_id(telegram_id)

    if user:
        # Обновляем существующего
        user.username = telegram_user.get('username', user.username)
        user.first_name = telegram_user.get('first_name', user.first_name)
        user.last_name = telegram_user.get('last_name', user.last_name)
        user.photo_url = telegram_user.get('photo_url', user.photo_url)
        db.session.commit()
        return user

    # Создаем нового
    user = User(
        telegram_id=telegram_id,
        username=telegram_user.get('username'),
        first_name=telegram_user.get('first_name', ''),
        last_name=telegram_user.get('last_name', ''),
        photo_url=telegram_user.get('photo_url')
    )
    db.session.add(user)
    db.session.commit()
    return user

def register(username, password):
    _newby = db.session.query(Users).filter(Users.username == username).first()
    
    if _newby:
        return jsonify({"status": "error", "message": "Имя занято"})

    _uuid = uuid.uuid4()
    db.session.add(Users(id_public=str(_uuid), username=username, password=password))
    db.session.commit()
    
    return jsonify({"status": "ok"})
    


def login(username, password):
    _user = db.session.query(Users).filter(Users.username == username).first()

    if not _user:
        return jsonify({"status": "error", "message": "Неправильный логин"})
    if not _user.password == password:
        return jsonify({"status": "error", "message": "Неправильный пароль"})
    
    session["id"] = _user.id
    session["id_public"] = _user.id_public
    session["name"] = _user.username
    session["role"] = 'admin'

    return jsonify({"status": "ok", "data": {"id" : str(_user.id_public), "name" : _user.username, "role" : 'admin', 'isAdmin' : True}})

def _info(_id_public, _name, _role):
    return jsonify({"status": "ok", "data": {"id" : str(_id_public) if _id_public else None , "name" : _name, "role" : _role, 'isAdmin' : True}})

def logout():
    session.pop('id', None)
    session.pop('id_public', None)
    session.pop('name', None)
    session.pop('role', None)
    return jsonify({"status": "ok"})

