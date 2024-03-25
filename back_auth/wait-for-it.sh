#!/bin/sh
# wait-for-it.sh

set -e

host="$1"
shift
port="$1"
shift
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -p "$port" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' >/dev/null 2>&1; do
	>&2 echo "Postgres is unavailable - sleeping"
	sleep 1
done

>&2 echo "Postgres is up - executing command"

python3 transcendence_django/manage.py makemigrations
python3 transcendence_django/manage.py migrate

echo "command is " $cmd

exec $cmd
