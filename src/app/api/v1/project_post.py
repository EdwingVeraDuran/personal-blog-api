from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project_post import ProjectPostOut
from app.services import project_posts as project_post_service


router = APIRouter()


@router.get("/projects/{project_slug}/posts", response_model=list[ProjectPostOut])
def list_project_posts(project_slug: str, db: Session = Depends(get_db)):
    return project_post_service.list_posts_by_project_slug(
        db, project_slug=project_slug, only_published=True
    )


@router.get("/projects/{project_slug}/posts/{post_slug}", response_model=ProjectPostOut)
def get_project_post(project_slug: str, post_slug: str, db: Session = Depends(get_db)):
    post = project_post_service.get_post_by_slug(
        db, project_slug=project_slug, post_slug=post_slug, only_published=True
    )
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post
