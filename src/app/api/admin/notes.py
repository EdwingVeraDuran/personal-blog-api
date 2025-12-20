from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin
from app.schemas.note import NoteAdminOut, NoteCreate, NoteUpdate
from app.services import notes as note_service

router = APIRouter(dependencies=[Depends(require_admin)])


@router.get("/notes", response_model=list[NoteAdminOut])
def list_notes(db: Session = Depends(get_db)):
    return note_service.list_notes(db, only_published=False)


@router.get("/notes/{note_id}", response_model=NoteAdminOut)
def get_note(note_id: str, db: Session = Depends(get_db)):
    note = note_service.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    return note


@router.post("/notes", response_model=NoteAdminOut, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)):
    return note_service.create_note(db, payload)


@router.patch("/notes/{note_id}", response_model=NoteAdminOut)
def update_note(note_id: str, payload: NoteUpdate, db: Session = Depends(get_db)):
    note = note_service.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    return note_service.update_note(db, note, payload)


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str, db: Session = Depends(get_db)):
    note = note_service.get_note_by_id(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="note not found")
    note_service.delete_note(db, note)
