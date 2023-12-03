from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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

class ListPlaylist(_message.Message):
    __slots__ = ["playlist"]
    PLAYLIST_FIELD_NUMBER: _ClassVar[int]
    playlist: _containers.RepeatedCompositeFieldContainer[PlaylistName]
    def __init__(self, playlist: _Optional[_Iterable[_Union[PlaylistName, _Mapping]]] = ...) -> None: ...

class PlaylistGroup(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

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
