from fastapi import APIRouter

from app.api.admin import auth, project_posts, projects

router = APIRouter()

router.include_router(auth.router, tags=["admin:auth"])
router.include_router(projects.router, tags=["admin:projects"])
router.include_router(project_posts.router, tags=["admin:project-posts"])
