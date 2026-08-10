from flask import Flask
from flask_cors import CORS

from endpoints import user, game

from db import db
from scr.core import settings

app = Flask(__name__)
app.config.from_object(settings)


CORS(app, supports_credentials=True, cors_allowed_origins="*")
db.init_app(app)

app.register_blueprint(user.bp)
app.register_blueprint(game.bp)

@app.cli.command('reset-db')
def reset_db_command():
    """Сбросить и пересоздать базу данных."""
    db.drop_all()
    db.create_all()
    click.echo('✅ База данных пересоздана!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)