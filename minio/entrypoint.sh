#!/bin/bash

minio server /data --console-address ":9001" &

MINIO_PID=$!

sleep 10

mc alias set myminio https://127.0.0.1:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD --insecure
mc mb myminio/avatars
mc cp /media/default_avatar.jpg myminio/avatars/default_avatar.jpg

wait $MINIO_PID
