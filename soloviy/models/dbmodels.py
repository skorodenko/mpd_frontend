import datetime
from soloviy.db import memory_db, db, BaseModel, BaseMemoryModel
from peewee import CharField, IntegerField, BooleanField, ForeignKeyField, FloatField, TimestampField, DateTimeField


class PlaylistTile(BaseModel):
    name = CharField(primary_key=True)
    sort_by = CharField(null = True)
    tile_order = TimestampField(default = datetime.datetime.now)
    active = BooleanField(default = False)
    locked = BooleanField(default = False)
    

class Playlist(BaseMemoryModel):
    playlist_name = CharField()
    file = CharField()
    time = IntegerField()
    duration = FloatField()  
    last_modified = DateTimeField(null = True)
    format = CharField(null = True)
    artist = CharField(null = True)
    albumartist = CharField(null = True)
    title = CharField(null = True)
    album = CharField(null = True)
    track = CharField(null = True)
    date = IntegerField(null = True)
    genre = CharField(null = True)
    composer = CharField(null = True)
    disc = IntegerField(null = True)
    

db.create_tables([PlaylistTile])
memory_db.create_tables([Playlist])