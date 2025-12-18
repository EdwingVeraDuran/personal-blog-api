from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import OptionalSlugStr, SlugStr


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1)
    repo_url: str | None = Field(default=None, max_length=500)
    demo_url: str | None = Field(default=None, max_length=500)


class ProjectCreate(ProjectBase):
    slug: str = SlugStr
    status: Literal["active", "archived"] | None = None


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    summary: str | None = Field(default=None, min_length=1)
    repo_url: str | None = Field(default=None, max_length=500)
    demo_url: str | None = Field(default=None, max_length=500)
    slug: str | None = OptionalSlugStr
    status: Literal["active", "archived"] | None = None


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str


class ProjectAdminOut(ProjectOut):
    status: Literal["active", "archived"]
    created_at: datetime
    updated_at: datetime
