#!/bin/sh
# wait-for-it.sh

set -e

cmd="$*"

python3 manage.py makemigrations
python3 manage.py migrate
python manage.py createsuperuser --no-input || true

echo "command is " "$cmd"

exec $cmd
