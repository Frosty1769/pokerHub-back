from flask import Flask
from flask_cors import CORS
from db import db
from endpoints.auth import auth_bp
from endpoints.user import user_bp  # ваш существующий
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация БД
    db.init_app(app)

    # CORS - настройте под себя
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Регистрация Blueprint'ов
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)  # ваш существующий

    # Создание таблиц
    with app.app_context():
        db.create_all()

    return app


@app.cli.command('reset-db')
def reset_db_command():
    """Сбросить и пересоздать базу данных."""
    db.drop_all()
    db.create_all()
    click.echo('✅ База данных пересоздана!')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)


