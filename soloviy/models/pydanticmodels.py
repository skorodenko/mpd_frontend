import datetime
from typing import Optional
from pydantic import BaseModel, Field, FieldValidationInfo, field_validator


class Library(BaseModel):
    file: str
    time: int
    duration: float
    directory: Optional[str] = Field(validate_default=True, default=None)
    lastmodified: datetime.datetime = Field(alias="last-modified")
    format: Optional[str] = None
    artist: Optional[str] = None
    albumartist: Optional[str] = None
    title: Optional[str] = None
    album: Optional[str] = None
    track: Optional[str] = None
    date: Optional[str] = None
    genre: Optional[str] = None
    composer: Optional[str] = None
    disc: Optional[int] = None

    @field_validator("artist", "albumartist", "genre", "composer", mode="before")
    @classmethod
    def _list_of_x_to_str(cls, val: str | list, info: FieldValidationInfo):
        if isinstance(val, list):
            return ",".join(val)
        return val

    @field_validator("directory")
    @classmethod
    def _directory_from_context(cls, val: str, info: FieldValidationInfo):
        context = info.context
        return context["directory"]