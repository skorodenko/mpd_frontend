#!/usr/bin/sh
SRC="./soloviy/backend/protobufs"
mkdir $SRC/lib
protoc -I $SRC --python_betterproto_out $SRC/lib $SRC/*.proto