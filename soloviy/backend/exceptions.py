from enum import IntEnum
from attrs import define


class Status(IntEnum):
    NOT_FOUND = 1
    BAD_REQUEST = 2


@define
class TMPDException(Exception):
    status: Status
    message: str = ""
