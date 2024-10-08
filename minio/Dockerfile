FROM minio/minio:RELEASE.2024-09-09T16-59-28Z-cpuv1

RUN mkdir -p /root/.minio/certs

COPY entrypoint.sh /bin/entrypoint.sh
COPY ssl/* /root/.minio/certs
COPY default_avatar.jpg /media

RUN chmod +x /bin/entrypoint.sh

HEALTHCHECK --interval=5s --timeout=1s --retries=20 CMD mc ready data/avatars --insecure

ENTRYPOINT ["/bin/entrypoint.sh"]