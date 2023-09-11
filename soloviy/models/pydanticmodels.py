import pydantic
import datetime
from typing import Optional


class Playlist(pydantic.BaseModel):
    playlist_name: str
    file: str
    time: int
    duration: float
    last_modified: datetime.datetime = pydantic.Field(alias="last-modified")
    format: Optional[str] = None
    artist: Optional[str] = None
    albumartist: Optional[str] = None
    title: Optional[str] = None
    album: Optional[str] = None
    track: Optional[str] = None
    date: Optional[int] = None
    genre: Optional[str] = None
    composer: Optional[str] = None
    disc: Optional[int] = None