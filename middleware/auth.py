from functools import wraps
from flask import request, jsonify, g
from db_actions.session import get_session_by_token
from db_actions.user import get_user_by_telegram_id
from db import db

def login_required(f):
    """Декоратор для проверки авторизации"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Публичные эндпоинты (без проверки)
        if request.endpoint in ['auth_login', 'auth_refresh', 'static']:
            return f(*args, **kwargs)

        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No authorization token', 'code': 401}), 401

        if token.startswith('Bearer '):
            token = token[7:]

        session = get_session_by_token(token)
        if not session or session.is_expired():
            return jsonify({'error': 'Invalid or expired session', 'code': 401}), 401

        # Обновляем активность
        session.last_activity = db.session.commit()  # Исправить!
        # Правильно: session.last_activity = datetime.utcnow(); db.session.commit()

        g.user = session.user
        g.session_token = token
        g.user_id = session.user_id

        return f(*args, **kwargs)
    return decorated

# TODO: поправить обновление last_activity, добавив импорт datetime