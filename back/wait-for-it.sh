#!/bin/sh
# wait-for-it.sh

set -e

cmd="$*"

python3 manage.py makemigrations transcendence_django
python3 manage.py migrate transcendence_django

echo "command is " "$cmd"
export DJANGO_SETTINGS_MODULE=transcendence_django.settings
exec $cmd
