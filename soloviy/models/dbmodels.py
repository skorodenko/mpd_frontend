from peewee import CharField, AutoField, ForeignKeyField
from soloviy.db import BaseModel



class ActivePlaylists(BaseModel):
    id = AutoField(primary_key = True)
    name = CharField()
