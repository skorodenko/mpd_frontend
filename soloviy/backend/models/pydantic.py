import uuid
import datetime
from typing import Optional
from soloviy.backend.db import state
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
 
 
class MetaTile(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    locked: bool = False
    group_by: str = Field(default_factory=lambda: state["group_by"])
    order_by_col: str = "track"
    order_by_asc: bool = True
    playing_pos: Optional[int] = None
    
    
#class Status(BaseModel):
#    partition: str
#    volume: float
#    repeat: int
#    random: int
#    single: int
#    consume: int
#    playlist: int
#    playlistlength: int
#    state: str
#    song: int
#    songid: int