FROM alpine:3.18

RUN apk add --no-cache minio-client netcat-openbsd curl

RUN curl -O http://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x mc && \
    mv mc /usr/local/bin/

COPY . .

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
