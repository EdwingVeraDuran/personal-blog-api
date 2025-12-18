from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def list_projects(db: Session, only_active: bool = True) -> list[Project]:
    stmt = select(Project)
    if only_active:
        stmt = stmt.where(Project.status == "active")
    return list(db.scalars(stmt).all())


def get_project_by_id(db: Session, project_id: str) -> Project | None:
    return db.get(Project, project_id)


def get_project_by_slug(db: Session, slug: str) -> Project | None:
    stmt = select(Project).where(Project.slug == slug)
    return db.scalars(stmt).first()


def create_project(db: Session, payload: ProjectCreate) -> Project:
    data = payload.model_dump()
    if data.get("status") is None:
        data.pop("status", None)
    project = Project(**data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def update_project(db: Session, project: Project, payload: ProjectUpdate) -> Project:
    data = payload.model_dump(exclude_unset=True)
    if data.get("status") is None:
        data.pop("status", None)
    for field, value in data.items():
        setattr(project, field, value)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
