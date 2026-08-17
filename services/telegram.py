from schemas.auth import InitData
import logging

logger = logging.getLogger(__name__)
class TelegramService:
    @staticmethod
    def validate_init_data(init_data: dict):
        """Валидирует данные инициализации от Telegram"""
        validated = InitData(**init_data)
        return validated.user.dict()