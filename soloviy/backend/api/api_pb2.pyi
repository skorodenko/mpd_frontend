from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Connected: _ClassVar[ConnectionStatus]
    FailedToConnect: _ClassVar[ConnectionStatus]
    NoMpdBinary: _ClassVar[ConnectionStatus]
Connected: ConnectionStatus
FailedToConnect: ConnectionStatus
NoMpdBinary: ConnectionStatus

class ConnectCredentials(_message.Message):
    __slots__ = ["socket", "password"]
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    socket: str
    password: str
    def __init__(self, socket: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class ConnectionDetails(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: ConnectionStatus
    def __init__(self, status: _Optional[_Union[ConnectionStatus, str]] = ...) -> None: ...

class UUID(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    def __init__(self, value: _Optional[bytes] = ...) -> None: ...

class ListMetaTile(_message.Message):
    __slots__ = ["metatile"]
    METATILE_FIELD_NUMBER: _ClassVar[int]
    metatile: _containers.RepeatedCompositeFieldContainer[MetaTile]
    def __init__(self, metatile: _Optional[_Iterable[_Union[MetaTile, _Mapping]]] = ...) -> None: ...

class PlaylistName(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ListPlaylistName(_message.Message):
    __slots__ = ["playlist"]
    PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    playlist: _containers.RepeatedCompositeFieldContainer[PlaylistName]
    def __init__(self, playlist: _Optional[_Iterable[_Union[PlaylistName, _Mapping]]] = ...) -> None: ...

class PlaylistGroup(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Playlist(_message.Message):
    __slots__ = ["song"]
    SONG_FIELD_NUMBER: _ClassVar[int]
    song: _containers.RepeatedCompositeFieldContainer[Song]
    def __init__(self, song: _Optional[_Iterable[_Union[Song, _Mapping]]] = ...) -> None: ...

class Song(_message.Message):
    __slots__ = ["id", "directory", "file", "time", "duration", "lastmodified", "format", "artist", "albumartist", "title", "album", "track", "date", "genre", "composer", "disc"]
    ID_FIELD_NUMBER: _ClassVar[int]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    LASTMODIFIED_FIELD_NUMBER: _ClassVar[int]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    ARTIST_FIELD_NUMBER: _ClassVar[int]
    ALBUMARTIST_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ALBUM_FIELD_NUMBER: _ClassVar[int]
    TRACK_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    GENRE_FIELD_NUMBER: _ClassVar[int]
    COMPOSER_FIELD_NUMBER: _ClassVar[int]
    DISC_FIELD_NUMBER: _ClassVar[int]
    id: int
    directory: str
    file: str
    time: int
    duration: float
    lastmodified: _timestamp_pb2.Timestamp
    format: str
    artist: str
    albumartist: str
    title: str
    album: str
    track: int
    date: str
    genre: str
    composer: str
    disc: int
    def __init__(self, id: _Optional[int] = ..., directory: _Optional[str] = ..., file: _Optional[str] = ..., time: _Optional[int] = ..., duration: _Optional[float] = ..., lastmodified: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., format: _Optional[str] = ..., artist: _Optional[str] = ..., albumartist: _Optional[str] = ..., title: _Optional[str] = ..., album: _Optional[str] = ..., track: _Optional[int] = ..., date: _Optional[str] = ..., genre: _Optional[str] = ..., composer: _Optional[str] = ..., disc: _Optional[int] = ...) -> None: ...

class MetaTile(_message.Message):
    __slots__ = ["name", "locked", "order_by_col", "order_by_asc"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_COL_FIELD_NUMBER: _ClassVar[int]
    ORDER_BY_ASC_FIELD_NUMBER: _ClassVar[int]
    name: str
    locked: bool
    order_by_col: str
    order_by_asc: str
    def __init__(self, name: _Optional[str] = ..., locked: bool = ..., order_by_col: _Optional[str] = ..., order_by_asc: _Optional[str] = ...) -> None: ...
