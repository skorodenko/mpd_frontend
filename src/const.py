from src.service.lib.tmpd import SongField


ALLOWED_GROUP_BY = [
    SongField.directory,
    SongField.artist, SongField.albumartist,
    SongField.album, SongField.date,
    SongField.genre, SongField.composer,
]