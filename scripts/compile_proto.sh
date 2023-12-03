#!/usr/bin/sh
SRC="./soloviy/backend"
DST="./soloviy/backend/api"
python -m grpc_tools.protoc -I $SRC --python_out $DST --pyi_out $DST --grpc_python_out $DST $SRC/api.proto