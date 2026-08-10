from db import db
from sqlalchemy.dialects.sqlite import TEXT, INTEGER, BOOLEAN
from sqlalchemy.sql.schema import ForeignKey
import sqlalchemy as sa

from enums.weapon_spell import AttackType, DamageType, HoldType, SpellType


class Users(db.Model):
    id = db.Column(INTEGER,autoincrement=True, primary_key=True, nullable=False)
    id_public = db.Column(TEXT(32), nullable=False)
    username = db.Column(TEXT, nullable=False, unique=True)
    password = db.Column(TEXT, nullable=False) 

class Games(db.Model):
    id = db.Column(INTEGER,autoincrement=True, primary_key=True, nullable=False)
    id_public = db.Column(TEXT(32), nullable=False)
    name = db.Column(TEXT, nullable=False)
    description = db.Column(TEXT, nullable=False)
    max_players = db.Column(INTEGER, nullable=False)
    deposit = db.Column(INTEGER, nullable=False)

class Registration(db.Model):
    id = db.Column(INTEGER,autoincrement=True, primary_key=True, nullable=False)
    id_user = db.Column(TEXT(32), nullable=False)
    id_game = db.Column(TEXT(32), nullable=False)
    is_approved = db.Column(BOOLEAN, nullable=False)
    



