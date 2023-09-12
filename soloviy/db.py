from rocksdict import Rdict
from peewee import Model, SqliteDatabase
from soloviy.config import sqlite_db, state_db


db = SqliteDatabase(sqlite_db, 
                    pragmas={
                        "journal_mode": "wal",
                    })

state = Rdict(state_db)


class BaseModel(Model):
    class Meta:
        database = db
        