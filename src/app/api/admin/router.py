from fastapi import APIRouter

from app.api.admin import auth, projects

router = APIRouter()

router.include_router(auth.router, tags=["admin:auth"])
router.include_router(projects.router, tags=["admin:projects"])
