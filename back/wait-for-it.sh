#!/bin/sh
# wait-for-it.sh

set -e

cmd="$*"

python3 manage.py makemigrations
python3 manage.py migrate

echo "command is " "$cmd"
export DJANGO_SETTINGS_MODULE=transcendence_django.settings
exec $cmd
