from fastapi import APIRouter

from app.api.admin import projects

router = APIRouter()

router.include_router(projects.router, tags=["admin:projects"])
