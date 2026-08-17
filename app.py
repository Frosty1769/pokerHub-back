from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate  
from db import db
from endpoints.auth import auth_bp
import click 
from scr.core import settings
import os
import logging

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

@app.before_request
def log_request():
    app.logger.info(f"📩 {request.method} {request.path} от {request.remote_addr}")

@app.after_request
def log_response(response):
    app.logger.info(f"✅ {request.method} {request.path} → {response.status_code}")
    return response



@app.cli.command('reset-db')
def reset_db_command():
    """Сбросить и пересоздать базу данных."""
    db.drop_all()
    db.create_all()
    click.echo('✅ База данных пересоздана!')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


