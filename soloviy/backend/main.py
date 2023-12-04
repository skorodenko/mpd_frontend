import grpc
import attrs
import asyncio
import logging
from soloviy.backend.api import api_pb2_grpc
from soloviy.backend.services.mpd import MpdService


logger = logging.getLogger("soloviy.backend.main")


@attrs.define
class Backend:
    addr: str = "[::]:50051"
    server: grpc.aio.Server = attrs.Factory(grpc.aio.server) 
    mpd: MpdService = attrs.Factory(MpdService)
    
    async def serve(self):
        api_pb2_grpc.add_MpdAPIServicer_to_server(
            self.mpd, self.server
        )
        self.server.add_insecure_port(self.addr)
        await self.server.start()
        logger.info("Started backend server")
        await self.server.wait_for_termination()
    
    async def graceful_shutdown(self):
        await self.server.stop(5)
        self.mpd.graceful_close()
 
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    backend = Backend()
    try:
        loop.run_until_complete(backend.serve())
    finally:
        loop.run_until_complete(backend.graceful_shutdown())
        loop.close()