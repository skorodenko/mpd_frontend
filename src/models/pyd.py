from enum import IntEnum
from datetime import datetime
from src.models import db
from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    ConfigDict,
    field_validator,
)


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ConnectionStatus(IntEnum):
    """Status of mpd connection"""

    Connected = 1
    FailedToConnect = 2
    NoMpdBinary = 3


class SortOrder(IntEnum):
    Ascending = 1
    Descending = 2


class SongField(IntEnum):
    file = 1
    time = 2
    duration = 3
    lastmodified = 4
    format = 5
    artist = 6
    albumartist = 7
    title = 8
    album = 9
    track = 10
    date = 11
    genre = 12
    composer = 13
    disc = 14
    directory = 15


class ConnectionCredentials(Base):
    """Credentials to connect to mpd"""

    socket: str | None = None
    password: str | None = None


class Song(Base):
    file: str
    time: int
    duration: float
    lastmodified: datetime | None = Field(alias="last-modified", default=None)
    format: str = ""
    artist: str = ""
    albumartist: str = ""
    title: str = ""
    album: str = ""
    track: int | None = None
    date: int | None = None
    genre: str = ""
    composer: str = ""
    disc: int | None = None

    @field_validator("artist", "albumartist", "genre", "composer", mode="before")
    @classmethod
    def _list_of_x_to_str(cls, val: str | list, info: ValidationInfo):
        if isinstance(val, list):
            return ", ".join(val)
        return val


class MetaPlaylist(Base):
    uuid: str | None = None
    name: str | None = None
    sort_by: SongField = SongField.track
    sort_order: SortOrder = SortOrder.Ascending
    group_by: SongField = SongField.directory
    locked: bool = False

    def db_playlist_query(self):
        query = db.Song.select().join(db.Tile)
        query = query.where(db.Song.tile.uuid == self.uuid)
        match self.sort_by:
            case SongField.directory:
                sort_order = getattr(db.Song, "track")
            case sort_by:
                sort_order = getattr(db.Song, sort_by.name)
        match self.sort_order:
            case SortOrder.Ascending:
                sort_order = sort_order
            case SortOrder.Descending:
                sort_order = -sort_order
        return query.order_by(sort_order)

    def mpd_playlist_query(self):
        sort_order = ""
        match self.sort_by:
            case SongField.directory:
                sort_order = "track"
            case sort_by:
                sort_order = sort_by.name
        match self.sort_order:
            case SortOrder.Ascending:
                sort_order = sort_order  # noqa: E731
            case SortOrder.Descending:
                sort_order = "-" + sort_order  # noqa: E731
        match self.name, self.group_by:
            case (None, _):
                raise ValueError("MPD playlist query should have 'name' and 'group'")
            case (name, SongField.directory):
                return [
                    f"(base '{name}')",
                    "sort",
                    sort_order,
                ]
            case (name, group_by):
                return [
                    f"({group_by.name} == '{name}')",
                    "sort",
                    sort_order,
                ]
