from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
import hashlib
import hmac
import os
from datetime import datetime

class TelegramUserData(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    photo_url: Optional[str] = None

class InitData(BaseModel):
    query_id: Optional[str] = None
    user: TelegramUserData
    auth_date: str
    hash: str
    start_param: Optional[str] = None
    chat_type: Optional[str] = None
    chat_instance: Optional[str] = None
    signature: Optional[str] = None 
    
    class Config:
        populate_by_name = True
        extra = 'allow'  # Разрешить дополнительные поля


    @validator('hash')
    def validate_telegram_hash(cls, v, values):
        bot_token = os.getenv('BOT_TOKEN')
        if not bot_token:
            raise ValueError('BOT_TOKEN not configured')

        # Собираем данные для проверки
        data = values.get('data', {})
        check_string = '\n'.join([
            f"{k}={v}" for k, v in sorted(data.items())
            if k != 'hash'
        ])

        secret_key = hashlib.sha256(bot_token.encode()).digest()
        computed_hash = hmac.new(
            secret_key,
            check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if computed_hash != v:
            raise ValueError('Invalid hash signature')

        # Проверка на "свежесть" данных (24 часа)
        auth_date = int(data.get('auth_date', 0))
        if datetime.utcnow().timestamp() - auth_date > 86400:
            raise ValueError('Auth data expired')

        return v

class LoginRequest(BaseModel):
    initData: Dict[str, Any]

class RefreshRequest(BaseModel):
    session_token: str

class AuthResponse(BaseModel):
    session_token: str
    user: Dict[str, Any]
    expires_at: datetime