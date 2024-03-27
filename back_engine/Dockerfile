FROM python:latest

RUN python3 -m venv venv

RUN pip install --upgrade pip
RUN pip install django django-cors-headers djangorestframework django-health-check channels_redis requests psycopg2-binary django-extensions
RUN python -m pip install -U 'channels[daphne]'
RUN pip install -U "Twisted[tls,http2]"
RUN pip install pytest pytest-asyncio pytest-django pytest-cov

RUN mkdir -p /var/run/back /etc/ssl

COPY ./ssl/* /etc/ssl/

COPY pong_game /var/run/back/pong_game
WORKDIR /var/run/back/pong_game

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT [ "sh", "entrypoint.sh" ]
#ENTRYPOINT ["daphne", "-b", "0.0.0.0", "-p", "8000", "-e", "ssl:443:privateKey=/etc/ssl/serv.key:certKey=/etc/ssl/serv.crt", "pong_game.asgi:application"]