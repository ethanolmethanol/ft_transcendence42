#!/bin/bash

minio server /data --address ":443" --console-address ":9001" &

MINIO_PID=$!

sleep 10

mc alias set data https://127.0.0.1:443 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD --insecure
mc mb data/avatars --insecure
mc cp /media/default_avatar.jpg data/avatars/default_avatar.jpg --insecure
mc anonymous set public data/avatars --insecure

wait $MINIO_PID
