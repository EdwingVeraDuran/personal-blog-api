from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import OptionalSlugStr, SlugStr


class TagBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class TagCreate(TagBase):
    slug: str = SlugStr


class TagUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    slug: str | None = OptionalSlugStr


class TagOut(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
