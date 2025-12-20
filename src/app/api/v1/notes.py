from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.note import NoteOut
from app.services import notes as note_service

router = APIRouter()


@router.get("/notes", response_model=list[NoteOut])
def list_notes(db: Session = Depends(get_db)):
    return note_service.list_notes(db, only_published=True)


@router.get("/notes/{note_slug}", response_model=NoteOut)
def get_note(note_slug: str, db: Session = Depends(get_db)):
    note = note_service.get_note_by_slug(db, slug=note_slug, only_published=True)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    return note
