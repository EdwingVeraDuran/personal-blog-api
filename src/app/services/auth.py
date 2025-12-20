from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenPair


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()


def authenticate(db: Session, credentials: LoginRequest) -> User | None:
    user = get_user_by_email(db, credentials.email)
    if not user:
        return None
    if not verify_password(credentials.password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user


def issue_tokens(user: User) -> TokenPair:
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    return TokenPair(access_token=access, refresh_token=refresh)


def users_count(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(User)) or 0


def create_admin_user(db: Session, email: str, password: str, role: str = "admin") -> User:
    user = User(
        email=email,
        password_hash=get_password_hash(password),
        role=role,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
