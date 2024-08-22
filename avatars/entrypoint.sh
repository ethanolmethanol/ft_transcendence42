#!/bin/sh

while ! nc -z minio 9000; do echo "Wait minio to startup..." && sleep 0.1; done; sleep 5

echo "Minio service is ready"

#/usr/local/bin/mc config host add myminio https://minio:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD
#/usr/local/bin/mc mb myminio/avatars
#/usr/local/bin/mc policy download myminio/avatars
#/usr/local/bin/mc cp /default_avatar.jpg myminio/avatars/default_avatar.jpg
#exit 0
tail -f /dev/null
