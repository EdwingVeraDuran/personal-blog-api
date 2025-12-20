from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.project_post import ProjectPost
from app.schemas.project_post import ProjectPostCreate, ProjectPostUpdate


def list_posts_by_project_slug(
    db: Session, project_slug: str, only_published: bool = True
) -> list[ProjectPost]:
    stmt = (
        select(ProjectPost)
        .join(Project)
        .where(Project.slug == project_slug)
    )
    if only_published:
        stmt = stmt.where(ProjectPost.status == "published")
    stmt = stmt.order_by(ProjectPost.published_at.desc().nullslast(), ProjectPost.created_at.desc())
    return list(db.scalars(stmt).all())


def list_posts(db: Session, project_id: str | None = None) -> list[ProjectPost]:
    stmt = select(ProjectPost)
    if project_id:
        stmt = stmt.where(ProjectPost.project_id == project_id)
    stmt = stmt.order_by(ProjectPost.created_at.desc())
    return list(db.scalars(stmt).all())


def get_post_by_slug(
    db: Session, project_slug: str, post_slug: str, only_published: bool = True
) -> ProjectPost | None:
    stmt = (
        select(ProjectPost)
        .join(Project)
        .where(Project.slug == project_slug, ProjectPost.slug == post_slug)
    )
    if only_published:
        stmt = stmt.where(ProjectPost.status == "published")
    return db.scalars(stmt).first()


def get_post_by_id(db: Session, post_id: str) -> ProjectPost | None:
    return db.get(ProjectPost, post_id)


def create_post(db: Session, payload: ProjectPostCreate) -> ProjectPost:
    data = payload.model_dump()
    post = ProjectPost(**data)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post: ProjectPost, payload: ProjectPostUpdate) -> ProjectPost:
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(post, field, value)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: ProjectPost) -> None:
    db.delete(post)
    db.commit()
