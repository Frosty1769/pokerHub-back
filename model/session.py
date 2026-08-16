from db import db
from datetime import datetime, timedelta
import secrets
from flask import current_app

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    session_token = db.Column(db.String(100), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    user_agent = db.Column(db.String(200))
    ip_address = db.Column(db.String(50))

    @classmethod
    def create(cls, user_id, user_agent=None, ip_address=None):
        """Создает новую сессию с TTL из конфига"""
        ttl = current_app.config.get('SESSION_TTL', timedelta(days=7))
        token = secrets.token_urlsafe(32)
        session = cls(
            user_id=user_id,
            session_token=token,
            expires_at=datetime.utcnow() + ttl,
            user_agent=user_agent,
            ip_address=ip_address
        )
        db.session.add(session)
        db.session.commit()
        return session

    def refresh(self):
        """Обновляет время жизни сессии"""
        ttl = current_app.config.get('SESSION_TTL', timedelta(days=7))
        self.expires_at = datetime.utcnow() + ttl
        self.last_activity = datetime.utcnow()
        db.session.commit()

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def invalidate(self):
        self.is_active = False
        db.session.commit()