#!/bin/sh

SRC_DIR='./src/protobuf'
DST_DIR='./src/protobuf/generated_classes'

mkdir -p $DST_DIR
protoc --proto_path=$SRC_DIR -I=$SRC_DIR --python_out=$DST_DIR --pyi_out=$DST_DIR $SRC_DIR/product.proto
