from peewee import Model, SqliteDatabase
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from soloviy.config import sqlite_db


tdb = TinyDB(storage=MemoryStorage)
db = SqliteDatabase(sqlite_db)


class BaseModel(Model):
    class Meta:
        database = db