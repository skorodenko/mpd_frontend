#!/usr/bin/sh
SRC="./src/service/protobufs"
DST="./src/service/lib"
mkdir $DST
protoc -I $SRC --python_betterproto_out $DST $SRC/*.proto