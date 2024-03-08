FROM python:latest

RUN apt-get update -y && apt-get install -y postgresql-client

RUN python3 -m venv venv

RUN pip install --upgrade pip

RUN pip install django django-cors-headers djangorestframework

# RUN pip install django-hurricane

RUN pip install psycopg2-binary

RUN mkdir /var/run/back

WORKDIR /var/run/back

COPY . /var/run/back

RUN chmod +x wait-for-it.sh

ENTRYPOINT ["./wait-for-it.sh", "db", "5432", "python3", "transcendence_django/manage.py", "runserver", "0.0.0.0:8000"]
