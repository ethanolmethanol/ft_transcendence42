FROM python:3

# Default healthcheck for image
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "python3" "transcendence_django/manage.py" "health_check" ]

RUN apt-get update -y && \
	apt-get install -y postgresql-client-15=15.6-0+deb12u1 --no-install-recommends && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*

RUN python3 -m venv venv

RUN pip install --no-cache-dir --upgrade pip==24.0 && \
	pip install --no-cache-dir django==5.0.3 django-cors-headers==4.3.1 \
		djangorestframework==3.14.0 django-health-check==3.18.1 \
		psycopg2-binary==2.9.9 werkzeug==3.0.1 django-extensions==3.2.3 pyOpenSSL==24.1.0

RUN mkdir -p /var/run/back /etc/ssl

COPY ./ssl/* /etc/ssl/
WORKDIR /var/run/back
COPY . /var/run/back
RUN chmod +x wait-for-it.sh
ENTRYPOINT ["./wait-for-it.sh", "db", "5432", "python3", "transcendence_django/manage.py", "runserver_plus", "--cert-file", "/etc/ssl/serv.crt", "--key-file", "/etc/ssl/serv.key", "0.0.0.0:8000"]