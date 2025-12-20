from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair
from app.services import auth as auth_service

router = APIRouter()


@router.post("/auth/login", response_model=TokenPair)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate(db, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    return auth_service.issue_tokens(user)


@router.post("/auth/token", response_model=TokenPair)
def login_with_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 password flow endpoint for Swagger "Authorize" button.
    Mirrors /auth/login but accepts form-data (username/password).
    """
    payload = LoginRequest(email=form_data.username, password=form_data.password)
    user = auth_service.authenticate(db, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    return auth_service.issue_tokens(user)


@router.post("/auth/refresh", response_model=TokenPair)
def refresh_tokens(payload: RefreshRequest, db: Session = Depends(get_db)):
    try:
        claims = security.decode_token(payload.refresh_token, expected_type="refresh")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid refresh token")

    user_id = claims["sub"]
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found or inactive")

    return auth_service.issue_tokens(user)


@router.post("/auth/bootstrap", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
def bootstrap_admin(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Create the initial admin user only if none exists.
    Returns tokens for immediate use.
    """
    if auth_service.users_count(db) > 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin already exists")

    user = auth_service.create_admin_user(db, email=payload.email, password=payload.password)
    return auth_service.issue_tokens(user)
