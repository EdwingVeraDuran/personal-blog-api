from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import SessionLocal

router = APIRouter()


@router.get("/health")
def health_check():
    response = {"status": "ok", "db": "ok"}
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        response["db"] = "unavailable"
        response["status"] = "degraded"

    return response
