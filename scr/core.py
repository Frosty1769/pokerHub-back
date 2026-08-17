from typing import ClassVar

from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

class Settings():

    SECRET_KEY: str = os.getenv('SECRET_KEY')
    CORS_ORIGINS: ClassVar[list[str]] = ["http://195.19.209.223/", "http://joker-hub.ru/", "https://joker-hub.ru/", "http://localhost:5173/"]    
    CORS_ALLOW_HEADERS: ClassVar[list[str]] = ["Content-Type", "Authorization"]
    SESSION_TYPE: str = "filesystem"
    SESSION_COOKIE_SAMESITE: str = "None"
    # SESSION_COOKIE_SAMESITE: str = "None"
    # SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_SECURE: bool = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    SQLALCHEMY_DATABASE_URI="sqlite:///pokerhub.db"


settings = Settings()
