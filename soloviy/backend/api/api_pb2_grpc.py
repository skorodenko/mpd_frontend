# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import api_pb2 as api__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class TilingAPIStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetTiles = channel.unary_unary(
                '/backend.api.TilingAPI/GetTiles',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=api__pb2.ListMetaTile.FromString,
                )
        self.AddTile = channel.unary_unary(
                '/backend.api.TilingAPI/AddTile',
                request_serializer=api__pb2.PlaylistName.SerializeToString,
                response_deserializer=api__pb2.MetaTile.FromString,
                )
        self.DelTile = channel.unary_unary(
                '/backend.api.TilingAPI/DelTile',
                request_serializer=api__pb2.MetaTile.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.UpdTile = channel.unary_unary(
                '/backend.api.TilingAPI/UpdTile',
                request_serializer=api__pb2.MetaTile.SerializeToString,
                response_deserializer=api__pb2.MetaTile.FromString,
                )


class TilingAPIServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetTiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddTile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DelTile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdTile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TilingAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetTiles': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTiles,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=api__pb2.ListMetaTile.SerializeToString,
            ),
            'AddTile': grpc.unary_unary_rpc_method_handler(
                    servicer.AddTile,
                    request_deserializer=api__pb2.PlaylistName.FromString,
                    response_serializer=api__pb2.MetaTile.SerializeToString,
            ),
            'DelTile': grpc.unary_unary_rpc_method_handler(
                    servicer.DelTile,
                    request_deserializer=api__pb2.MetaTile.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'UpdTile': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdTile,
                    request_deserializer=api__pb2.MetaTile.FromString,
                    response_serializer=api__pb2.MetaTile.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'backend.api.TilingAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TilingAPI(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetTiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/backend.api.TilingAPI/GetTiles',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            api__pb2.ListMetaTile.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddTile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/backend.api.TilingAPI/AddTile',
            api__pb2.PlaylistName.SerializeToString,
            api__pb2.MetaTile.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DelTile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/backend.api.TilingAPI/DelTile',
            api__pb2.MetaTile.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdTile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/backend.api.TilingAPI/UpdTile',
            api__pb2.MetaTile.SerializeToString,
            api__pb2.MetaTile.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class MpdAPIStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Connect = channel.unary_unary(
                '/backend.api.MpdAPI/Connect',
                request_serializer=api__pb2.ConnectCredentials.SerializeToString,
                response_deserializer=api__pb2.ConnectionDetails.FromString,
                )
        self.GetActiveGroup = channel.unary_unary(
                '/backend.api.MpdAPI/GetActiveGroup',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=api__pb2.PlaylistGroup.FromString,
                )
        self.GetPlaylists = channel.unary_unary(
                '/backend.api.MpdAPI/GetPlaylists',
                request_serializer=api__pb2.PlaylistGroup.SerializeToString,
                response_deserializer=api__pb2.ListPlaylistName.FromString,
                )


class MpdAPIServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Connect(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetActiveGroup(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPlaylists(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MpdAPIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Connect': grpc.unary_unary_rpc_method_handler(
                    servicer.Connect,
                    request_deserializer=api__pb2.ConnectCredentials.FromString,
                    response_serializer=api__pb2.ConnectionDetails.SerializeToString,
            ),
            'GetActiveGroup': grpc.unary_unary_rpc_method_handler(
                    servicer.GetActiveGroup,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=api__pb2.PlaylistGroup.SerializeToString,
            ),
            'GetPlaylists': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPlaylists,
                    request_deserializer=api__pb2.PlaylistGroup.FromString,
                    response_serializer=api__pb2.ListPlaylistName.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'backend.api.MpdAPI', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MpdAPI(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Connect(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/backend.api.MpdAPI/Connect',
            api__pb2.ConnectCredentials.SerializeToString,
            api__pb2.ConnectionDetails.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetActiveGroup(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/backend.api.MpdAPI/GetActiveGroup',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            api__pb2.PlaylistGroup.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPlaylists(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/backend.api.MpdAPI/GetPlaylists',
            api__pb2.PlaylistGroup.SerializeToString,
            api__pb2.ListPlaylistName.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
