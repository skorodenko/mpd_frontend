from soloviy.backend.db import db, BaseModel
from peewee import CharField, IntegerField, FloatField, DateTimeField, AutoField

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