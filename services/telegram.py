from schemas.auth import InitData

class TelegramService:
    @staticmethod
    def validate_init_data(init_data: dict):
        """Валидирует данные инициализации от Telegram"""
        validated = InitData(**init_data)
        return validated.user.dict()