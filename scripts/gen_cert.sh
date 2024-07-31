#!/bin/bash

CERT_DIR="ssl/"
CERT_PATH="${CERT_DIR}/serv.crt"
KEY_PATH="${CERT_DIR}/serv.key"
SSL_CONT_DIRS=(front/ssl back/ssl)

if [ "$1" = "clean" ]; then
	rm -rf "${CERT_DIR}" "${SSL_CONT_DIRS[@]}"
	exit 0
fi

if [ ! -e "${CERT_DIR}" ]; then
	~/bin/mkcert serv localhost 127.0.0.1 ::1
	mkdir -p "${CERT_DIR}"
	mv ./serv+3.pem "${CERT_PATH}"
	mv ./serv+3-key.pem ./"${KEY_PATH}"
fi

for dir in "${SSL_CONT_DIRS[@]}"; do
	mkdir -p "$dir"
	cp -r "${CERT_DIR}" "$dir"
done
