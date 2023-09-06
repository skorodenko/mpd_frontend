from soloviy import logger
from tinydb import TinyDB
from tinydb.storages import MemoryStorage


db = TinyDB(storage=MemoryStorage)