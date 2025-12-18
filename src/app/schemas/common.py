from pydantic import Field

SlugStr = Field(
    min_length=1,
    max_length=255,
    pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
)

OptionalSlugStr = Field(
    default=None,
    min_length=1,
    max_length=255,
    pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
)

CommitShaStr = Field(
    min_length=7,
    max_length=40,
    pattern=r"^[0-9a-fA-F]{7,40}$",
)

OptionalCommitShaStr = Field(
    default=None,
    min_length=7,
    max_length=40,
    pattern=r"^[0-9a-fA-F]{7,40}$",
)
