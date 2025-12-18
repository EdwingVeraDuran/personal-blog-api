from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import OptionalSlugStr, SlugStr


class NoteBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1)
    content_md: str = Field(min_length=1)
    category: str | None = Field(default=None, max_length=100)


class NoteCreate(NoteBase):
    slug: str = SlugStr


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    summary: str | None = Field(default=None, min_length=1)
    content_md: str | None = Field(default=None, min_length=1)
    category: str | None = Field(default=None, max_length=100)
    slug: str | None = OptionalSlugStr
    status: Literal["draft", "published"] | None = None


class NoteOut(NoteBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    published_at: datetime | None = None


class NoteAdminOut(NoteOut):
    status: Literal["draft", "published"]
    created_at: datetime
    updated_at: datetime
