from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import OptionalCommitShaStr, OptionalSlugStr, SlugStr


class ProjectPostBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    summary: str = Field(min_length=1)
    content_md: str = Field(min_length=1)
    version: str | None = Field(default=None, max_length=100)
    commit_sha: str | None = OptionalCommitShaStr


class ProjectPostCreate(ProjectPostBase):
    project_id: UUID
    slug: str = SlugStr


class ProjectPostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    summary: str | None = Field(default=None, min_length=1)
    content_md: str | None = Field(default=None, min_length=1)
    version: str | None = Field(default=None, max_length=100)
    commit_sha: str | None = OptionalCommitShaStr
    slug: str | None = OptionalSlugStr
    status: Literal["draft", "published"] | None = None


class ProjectPostOut(ProjectPostBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    published_at: datetime | None = None


class ProjectPostAdminOut(ProjectPostOut):
    project_id: UUID
    status: Literal["draft", "published"]
    created_at: datetime
    updated_at: datetime
