#!/bin/bash

export DJANGO_SETTINGS_MODULE=pong_game.settings

echo "Applying database migrations..."
python manage.py migrate
python manage.py makemigrations game
python manage.py migrate game

if [ $? -ne 0 ]; then
  echo "Failed to apply database migrations."
  exit 1
fi

echo "Starting Daphne server..."
daphne -b 0.0.0.0 -p 8000 -e ssl:443:privateKey=/etc/ssl/serv.key:certKey=/etc/ssl/serv.crt pong_game.asgi:application

if [ $? -ne 0 ]; then
  echo "Failed to start Daphne server."
  exit 1
fi
