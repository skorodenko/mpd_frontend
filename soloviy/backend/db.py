import datetime
from uuid import uuid4
from soloviy.config import sqlite_db
from peewee import (
    Model,
    SqliteDatabase,
    BooleanField,
    CharField,
    IntegerField,
    FloatField,
    DateTimeField,
    ForeignKeyField,
)


db = SqliteDatabase(
    sqlite_db,
    pragmas={
        "journal_mode": "wal",
        "foreign_keys": 1,
    },
)


class BaseModel(Model):
    class Meta:
        database = db


class Tile(BaseModel):
    uuid = CharField(primary_key=True, default=lambda: str(uuid4()))
    name = CharField()
    updated = DateTimeField(default=datetime.datetime.now)
    locked = BooleanField(default=False)
    sort_by = IntegerField()
    sort_order = IntegerField()
    group_by = IntegerField()


class Song(BaseModel):
    tile = ForeignKeyField(Tile, backref="songs", on_delete="cascade")
    file = CharField()
    time = IntegerField()
    duration = FloatField()
    lastmodified = DateTimeField()
    format = CharField()
    artist = CharField()
    albumartist = CharField()
    title = CharField()
    album = CharField()
    track = IntegerField(null=True)
    date = IntegerField(null=True)
    genre = CharField()
    composer = CharField()
    disc = IntegerField(null=True)


db.create_tables([Tile, Song])
