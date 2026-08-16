from model.session import Session
from db import db
from typing import Optional

def get_session_by_token(token: str) -> Optional[Session]:
    return Session.query.filter_by(
        session_token=token,
        is_active=True
    ).first()

def create_session(user_id: int, user_agent: str = None, ip_address: str = None) -> Session:
    return Session.create(user_id, user_agent, ip_address)

def refresh_session(session: Session) -> Session:
    session.refresh()
    return session

def invalidate_session(session: Session) -> None:
    session.invalidate()