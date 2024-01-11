#!/usr/bin/sh
SRC="./soloviy/backend/protobufs"
mkdir $SRC/lib
#python -m grpc_tools.protoc -I $SRC --python_betterproto_opt=pydantic_dataclasses --python_betterproto_out $SRC/lib $SRC/*.proto
python -m grpc_tools.protoc -I $SRC --python_betterproto_out $SRC/lib $SRC/*.proto