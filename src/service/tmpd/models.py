from typing import Optional
from datetime import datetime
from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    ConfigDict,
    field_validator,
)
from src.service.tmpd import db
from src.service.protobufs.lib.tmpd import SongField, SortOrder


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SongModel(Base):
    file: str
    time: int
    duration: float
    lastmodified: datetime = Field(alias="last-modified")
    format: Optional[str] = ""
    artist: Optional[str] = ""
    albumartist: Optional[str] = ""
    title: Optional[str] = ""
    album: Optional[str] = ""
    track: Optional[int] = ""
    date: Optional[int] = 0
    genre: Optional[str] = ""
    composer: Optional[str] = ""
    disc: Optional[int] = 0

    @field_validator("artist", "albumartist", "genre", "composer", mode="before")
    @classmethod
    def _list_of_x_to_str(cls, val: str | list, info: ValidationInfo):
        if isinstance(val, list):
            return ", ".join(val)
        return val


class MetaPlaylistModel(Base):
    uuid: str
    name: str
    sort_by: SongField
    sort_order: SortOrder
    group_by: SongField
    locked: bool

    def db_playlist_query(self):
        query = db.Song.select().join(db.Tile)
        query = query.where(db.Song.tile.uuid == self.uuid)
        match self.sort_by:
            case SongField.directory | SongField.none:
                sort_order = getattr(db.Song, "track")
            case sort_by:
                sort_order = getattr(db.Song, sort_by.name)
        match self.sort_order:
            case SortOrder.Ascending:
                sort_order = sort_order  # noqa: E731
            case SortOrder.Descending:
                sort_order = -sort_order  # noqa: E731
        return query.order_by(sort_order)

    def mpd_playlist_query(self):
        sort_order = ""
        match self.sort_by:
            case SongField.directory | SongField.none:
                sort_order = "track"
            case sort_by:
                sort_order = sort_by.name
        match self.sort_order:
            case SortOrder.Ascending:
                sort_order = sort_order  # noqa: E731
            case SortOrder.Descending:
                sort_order = "-" + sort_order  # noqa: E731
        match self.name, self.group_by:
            case ("", _) | (_, SongField.none):
                raise ValueError("MPD playlist query should have 'name' and 'group'")
            case name, SongField.directory:
                return [
                    f"(base '{name}')",
                    "sort",
                    sort_order,
                ]
            case name, group_by:
                return [
                    f"({group_by.name} == '{name}')",
                    "sort",
                    sort_order,
                ]
