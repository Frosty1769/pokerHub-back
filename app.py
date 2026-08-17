from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate  
from db import db
from endpoints.auth import auth_bp
import click 
from scr.core import settings
import os

app = Flask(__name__)
app.config.from_object(settings)

# Инициализация БД
db.init_app(app)

migrate = Migrate(app, db)
# CORS - настройте под себя
CORS(app, supports_credentials=True, cors_allowed_origins="*")
# Регистрация Blueprint'ов
app.register_blueprint(auth_bp)
# Создание таблиц
# with app.app_context():
#     db.create_all()



@app.cli.command('reset-db')
def reset_db_command():
    """Сбросить и пересоздать базу данных."""
    db.drop_all()
    db.create_all()
    click.echo('✅ База данных пересоздана!')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


