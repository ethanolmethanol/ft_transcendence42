FROM minio/minio:latest

RUN mkdir -p /root/.minio/certs

COPY entrypoint.sh /bin/entrypoint.sh
COPY ssl/* /root/.minio/certs
COPY default_avatar.jpg /media

RUN chmod +x /bin/entrypoint.sh

ENTRYPOINT ["/bin/entrypoint.sh"]