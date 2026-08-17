from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
import hashlib
import hmac
import json
import os
import re
from datetime import datetime
from urllib.parse import urlencode, parse_qs

import logging

logger = logging.getLogger(__name__)

class TelegramUserData(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    photo_url: Optional[str] = None
    
    class Config:
        populate_by_name = True
        extra = 'allow'  # Разрешить дополнительные поля

class InitData(BaseModel):
    query_id: Optional[str] = None
    user: TelegramUserData
    auth_date: str
    start_param: Optional[str] = None
    chat_type: str
    chat_instance: str
    signature: Optional[str] = None 
    hash: str
    
    class Config:
        populate_by_name = True
        extra = 'allow'  # Разрешить дополнительные поля


class LoginRequest(BaseModel):
    initData: Dict[str, Any]

class RefreshRequest(BaseModel):
    session_token: str

class AuthResponse(BaseModel):
    session_token: str
    user: Dict[str, Any]
    expires_at: datetime