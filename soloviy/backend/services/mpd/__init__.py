import attrs
import socket
import logging
import asyncio

from . import db
from . import utils
from pydantic import TypeAdapter
from subprocess import Popen
from typing import Optional, List
from betterproto.lib.google.protobuf import Empty
from mpd.asyncio import MPDClient
from soloviy.config import settings
from soloviy.backend.protobufs.lib import (
    ConnectionCredentials,
    ConnectionDetails,
    MpdServiceBase,
    ConnectionStatus,
)

logger = logging.getLogger(__name__)


@attrs.define
class MpdService(MpdServiceBase):
    mpd_binary: Optional[str] = attrs.field()
    mpd_server: Optional[Popen] = None
    mpd_client: MPDClient = attrs.Factory(MPDClient)

    @mpd_binary.default
    def _factory_mpd_binary(self) -> bool:
        from shutil import which

        binary = which("mpd")
        if binary:
            logger.debug(f"Found 'mpd' binary: {binary}")
        else:
            logger.debug("Mpd binary not found in PATH")
        return binary

    def close(self):
        logger.debug("Gracefully closing MpdService")
        if self.mpd_client.connected:
            self.mpd_client.disconnect()
        if self.mpd_server:
            self.mpd_server.terminate()
            self.mpd_server.wait(5)

    async def connect(
        self, connection_credentials: ConnectionCredentials
    ) -> ConnectionDetails:
        logger.debug("Establishing connection to mpd")
        if connection_credentials.socket == settings.mpd.native_socket:
            logger.debug("Starting mpd server instance")
            if self.mpd_binary:
                self.mpd_server = Popen(
                    [self.mpd_binary, settings.mpd.native_config, "--no-daemon"]
                )
                await asyncio.sleep(0.5)
            else:
                logger.warning("Mpd binary not found")
                return ConnectionDetails(ConnectionStatus.NoMpdBinary)
        try:
            _socket = connection_credentials.socket
            await self.mpd_client.connect(_socket)
            logger.debug(f"Successfuly connected to mpd: {_socket}")
            return ConnectionDetails(ConnectionStatus.Connected)
        except (socket.gaierror, ConnectionRefusedError):
            logger.warning(f"Failed to connect to mpd: {_socket}")
            return ConnectionDetails(ConnectionStatus.FailedToConnect)

    async def update_db(self, betterproto_lib_google_protobuf_empty: Empty) -> Empty:
        logger.debug("Started db update")
        await self.mpd_client.update()
        data = await self.mpd_client.listallinfo()
        data = utils.group_by_folders(data)
        for directory in data:
            ta = TypeAdapter(List[db.LibraryModel])
            sdata = data[directory]
            sdata = [i for i in sdata if i.get("file")]
            sdata = ta.validate_python(sdata, context={"directory": directory})
            sdata = ta.dump_python(sdata)
            db.Library.insert_many(sdata).execute()
        logger.debug("Ended db update")
        return Empty()
