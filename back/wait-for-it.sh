#!/bin/sh
# wait-for-it.sh

set -e

cmd="$*"

python3 manage.py makemigrations
python3 manage.py migrate

echo "command is " "$cmd"

exec $cmd
