from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin
from app.schemas.project_post import (
    ProjectPostAdminOut,
    ProjectPostCreate,
    ProjectPostUpdate,
)
from app.services import project_posts as project_post_service

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("/project-posts", response_model=list[ProjectPostAdminOut])
def list_project_posts(
    project_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return project_post_service.list_posts(db, project_id=project_id)


@router.get("/project-posts/{post_id}", response_model=ProjectPostAdminOut)
def get_project_post(post_id: str, db: Session = Depends(get_db)):
    post = project_post_service.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post


@router.post(
    "/project-posts",
    response_model=ProjectPostAdminOut,
    status_code=status.HTTP_201_CREATED,
)
def create_project_post(payload: ProjectPostCreate, db: Session = Depends(get_db)):
    return project_post_service.create_post(db, payload)


@router.patch("/project-posts/{post_id}", response_model=ProjectPostAdminOut)
def update_project_post(
    post_id: str, payload: ProjectPostUpdate, db: Session = Depends(get_db)
):
    post = project_post_service.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return project_post_service.update_post(db, post, payload)


@router.delete("/project-posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_post(post_id: str, db: Session = Depends(get_db)):
    post = project_post_service.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    project_post_service.delete_post(db, post)
