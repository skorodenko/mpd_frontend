import attrs
import asyncio
import logging
from grpclib.server import Server
from grpclib.utils import graceful_exit
from soloviy.backend.services.mpd import MpdService
from soloviy.config import settings


logger = logging.getLogger("soloviy.backend.main")


@attrs.define
class Backend:
    host: str = "localhost"
    port: int = settings.default.grpc_port
    mpd_service: MpdService = attrs.Factory(MpdService)
    grpc_server: Server = attrs.field()

    @grpc_server.default
    def _factory_grpc_server(self):
        services = [self.mpd_service]
        return Server(services)

    async def serve(self):
        with graceful_exit([self.grpc_server]):
            await self.grpc_server.start(self.host, self.port)
            await self.grpc_server.wait_closed()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    backend = Backend()
    loop.run_until_complete(backend.serve())
