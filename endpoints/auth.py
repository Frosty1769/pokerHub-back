from flask import request, jsonify, Blueprint, g
from schemas.auth import LoginRequest, RefreshRequest, AuthResponse
from services.telegram import TelegramService
from db_actions.user import create_or_update_user
from db_actions.session import create_session, get_session_by_token, refresh_session, invalidate_session
from middleware.auth import login_required
import logging
from scr.core import settings

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Вход через Telegram"""
    try:
        data = request.get_json()
        if not data or 'initData' not in data:
            return jsonify({'error': 'Missing initData'}), 400

        # 1. Валидируем данные Telegram
        init_data = data['initData']
        logger.debug(init_data)
        logger.debug("BOT_TOKEN", settings.BOT_TOKEN)
        logger.debug("SECRET_KEY", settings.SECRET_KEY)
        validated_user = TelegramService.validate_init_data(init_data)

        # 2. Создаем или обновляем пользователя в БД
        user = create_or_update_user(validated_user)

        # 3. Создаем сессию
        user_agent = request.headers.get('User-Agent')
        ip_address = request.remote_addr
        session = create_session(user.id, user_agent, ip_address)

        response = AuthResponse(
            session_token=session.session_token,
            user=user.to_dict(),
            expires_at=session.expires_at
        )
        return jsonify(response.dict()), 200

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Обновление сессии"""
    try:
        data = request.get_json()
        if not data or 'session_token' not in data:
            return jsonify({'error': 'Missing session_token'}), 400

        session = get_session_by_token(data['session_token'])
        if not session:
            return jsonify({'error': 'Session not found'}), 404

        if session.is_expired():
            # Создаем новую сессию вместо старой
            invalidate_session(session)
            new_session = create_session(
                session.user_id,
                request.headers.get('User-Agent'),
                request.remote_addr
            )
            response = AuthResponse(
                session_token=new_session.session_token,
                user=session.user.to_dict(),
                expires_at=new_session.expires_at
            )
            return jsonify({'refreshed': True, **response.dict()}), 200

        # Просто обновляем время жизни
        refresh_session(session)
        response = AuthResponse(
            session_token=session.session_token,
            user=session.user.to_dict(),
            expires_at=session.expires_at
        )
        return jsonify({'refreshed': False, **response.dict()}), 200

    except Exception as e:
        logger.error(f"Refresh error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Выход из системы"""
    try:
        session = get_session_by_token(g.session_token)
        if session:
            invalidate_session(session)
        return jsonify({'success': True}), 200
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    """Информация о текущем пользователе"""
    return jsonify({
        'user': g.user.to_dict(),
        'session_token': g.session_token
    }), 200