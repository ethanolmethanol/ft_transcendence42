FROM python:latest

RUN mkdir /var/run/back

WORKDIR /var/run/back

COPY . /var/run/back

RUN chmod +x wait-for-it.sh

RUN apt-get update -y && apt-get install -y postgresql-client

RUN python3 -m venv venv

RUN pip install --upgrade pip

RUN pip install django django-cors-headers

RUN pip install django-hurricane

RUN pip install psycopg2-binary

# CMD ["python3", "transcendence_django/manage.py", "runserver"]
