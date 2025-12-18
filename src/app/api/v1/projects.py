from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.project import ProjectOut
from app.services import projects as project_service

router = APIRouter()


@router.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return project_service.list_projects(db, only_active=True)


@router.get("/projects/{project_slug}", response_model=ProjectOut)
def get_project(project_slug: str, db: Session = Depends(get_db)):
    project = project_service.get_project_by_slug(db, project_slug)
    if not project:
        raise HTTPException(status_code=404, detail="project not found")
    return project
