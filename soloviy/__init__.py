from soloviy import logger
from soloviy.config import tinydb_file
from tinydb import TinyDB
from tinydb.storages import MemoryStorage


db = TinyDB(storage=MemoryStorage)