#!/bin/bash

get_ip() {
    ifconfig enp3s0f0 | grep 'inet ' | awk '{print $2}'
}

clean_up() {
    rm -rf "${CERT_DIR}" "${SSL_CONT_DIRS[@]}"
    exit 0
}

generate_certificates() {
    mkcert serv ${IP_ADDR} localhost 127.0.0.1 ::1
    mkdir -p "${CERT_DIR}"
    mv ./serv+4.pem "${CERT_PATH}"
    mv ./serv+4-key.pem "${KEY_PATH}"
}

distribute_certificates() {
    for dir in "${SSL_CONT_DIRS[@]}"; do
        mkdir -p "$dir"
        cp -r "${CERT_DIR}" "$dir"
    done
}

CERT_DIR="ssl/"
CERT_PATH="${CERT_DIR}/serv.crt"
KEY_PATH="${CERT_DIR}/serv.key"
SSL_CONT_DIRS=(front/ssl back/ssl)
IP_ADDR=$(get_ip)

if [ "$1" = "clean" ]; then
    clean_up
fi

if [ ! -e "${CERT_DIR}" ]; then
    generate_certificates
fi

distribute_certificates
