#!/bin/sh
# wait-for-it.sh

set -e

host="$1"
shift
port="$1"
shift
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -h "$port" -U "your_database_user" -c '\q'; do
 >&2 echo "Postgres is unavailable - sleeping"
 sleep 1
done

>&2 echo "Postgres is up - executing command"

python3 transcendence_django/manage.py migrate

exec $cmd