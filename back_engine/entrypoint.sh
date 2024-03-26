#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

if [ $? -ne 0 ]; then
  echo "Failed to apply database migrations."
  exit 1
fi

# Start Daphne server
echo "Starting Daphne server..."
daphne -b 0.0.0.0 -p 8000 -e ssl:443:privateKey=/etc/ssl/serv.key:certKey=/etc/ssl/serv.crt pong_game.asgi:application
