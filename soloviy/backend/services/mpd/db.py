from datetime import datetime
from soloviy.config import sqlite_db
from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    IntegerField,
    FloatField,
    DateTimeField,
    AutoField,
)
from typing import Optional
from pydantic import Field, field_validator, ValidationInfo
from pydantic.dataclasses import dataclass


db = SqliteDatabase(
    ":memory:",
    pragmas={
        "journal_mode": "wal",
    },
)


class BaseModel(Model):
    class Meta:
        database = db


@dataclass
class LibraryModel:
    file: str
    time: int
    duration: float
    directory: Optional[str] = Field(validate_default=True, default=None)
    lastmodified: datetime = Field(alias="last-modified")
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
    def _list_of_x_to_str(cls, val: str | list, info: ValidationInfo):
        if isinstance(val, list):
            return ",".join(val)
        return val

    @field_validator("directory")
    @classmethod
    def _directory_from_context(cls, val: str, info: ValidationInfo):
        context = info.context
        return context["directory"]


class Library(BaseModel):
    id = AutoField()
    directory = CharField()
    file = CharField()
    time = IntegerField()
    duration = FloatField()
    lastmodified = DateTimeField(null=True)
    format = CharField(null=True)
    artist = CharField(null=True)
    albumartist = CharField(null=True)
    title = CharField(null=True)
    album = CharField(null=True)
    track = IntegerField(null=True)
    date = IntegerField(null=True)
    genre = CharField(null=True)
    composer = CharField(null=True)
    disc = IntegerField(null=True)


db.create_tables([Library])
