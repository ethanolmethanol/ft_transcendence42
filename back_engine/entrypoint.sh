python manage.py migrate
daphne -b 0.0.0.0 -p 8000 -e ssl:443:privateKey=/etc/ssl/serv.key:certKey=/etc/ssl/serv.crt pong_game.asgi:application
