from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate


def list_notes(db: Session, only_published: bool = True) -> list[Note]:
    stmt = select(Note)
    if only_published:
        stmt = stmt.where(Note.status == "published")
    stmt = stmt.order_by(Note.published_at.desc().nullslast(), Note.created_at.desc())
    return list(db.scalars(stmt).all())


def get_note_by_slug(db: Session, slug: str, only_published: bool = True) -> Note | None:
    stmt = select(Note).where(Note.slug == slug)
    if only_published:
        stmt = stmt.where(Note.status == "published")
    return db.scalars(stmt).first()


def get_note_by_id(db: Session, note_id: str) -> Note | None:
    return db.get(Note, note_id)


def create_note(db: Session, payload: NoteCreate) -> Note:
    data = payload.model_dump()
    note = Note(**data)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def update_note(db: Session, note: Note, payload: NoteUpdate) -> Note:
    data = payload.model_dump(exclude_unset=True)
    new_status = data.get("status")

    for field, value in data.items():
        setattr(note, field, value)

    if new_status == "published" and note.published_at is None:
        note.published_at = datetime.now(timezone.utc)

    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note: Note) -> None:
    db.delete(note)
    db.commit()
