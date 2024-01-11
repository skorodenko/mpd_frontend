from soloviy.config import sqlite_db
from peewee import Model, SqliteDatabase, CharField, IntegerField, FloatField, DateTimeField, AutoField


db = SqliteDatabase(
    ":memory:", 
    pragmas={
        "journal_mode": "wal",
    }
)


class BaseModel(Model):
    class Meta:
        database = db


class Library(BaseModel):
    id = AutoField()
    directory = CharField()
    file = CharField()
    time = IntegerField()
    duration = FloatField()  
    lastmodified = DateTimeField(null = True)
    format = CharField(null = True)
    artist = CharField(null = True)
    albumartist = CharField(null = True)
    title = CharField(null = True)
    album = CharField(null = True)
    track = IntegerField(null = True)
    date = IntegerField(null = True)
    genre = CharField(null = True)
    composer = CharField(null = True)
    disc = IntegerField(null = True)
    

db.create_tables([Library])