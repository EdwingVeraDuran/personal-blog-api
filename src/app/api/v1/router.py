from fastapi import APIRouter

from app.api.v1 import health, project_post, projects

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(projects.router, tags=["projects"])
router.include_router(project_post.router, tags=["project-posts"])
