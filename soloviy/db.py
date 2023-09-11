from peewee import Model, SqliteDatabase
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from soloviy.config import sqlite_db


tdb = TinyDB(storage=MemoryStorage)
#db = SqliteDatabase(sqlite_db, 
#                    pragmas={
#                        "journal_mode": "wal",
#                    })
db = SqliteDatabase(":memory:")
memory_db = SqliteDatabase(":memory:")


class BaseModel(Model):
    class Meta:
        database = db
        
class BaseMemoryModel(Model):
    class Meta:
        database = memory_db