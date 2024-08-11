#!/bin/sh
# wait-for-it.sh

set -e

cmd="$*"

python3 manage.py makemigrations shared_models
python3 manage.py migrate shared_models
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py showmigrations

#celery -A transcendence_django worker --loglevel=info
#celery -A transcendence_django beat --loglevel=info

echo "command is " "$cmd"
exec $cmd
