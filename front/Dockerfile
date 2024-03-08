FROM node:alpine AS builder

WORKDIR /usr/src/app

RUN apk update
RUN apk upgrade
RUN apk add curl
RUN npm install -g @angular/cli

RUN npm install
RUN npm build

FROM nginx:alpine

RUN apk update && apk upgrade && apk add openssl curl

RUN rm -rf /usr/share/nginx/html/*

COPY ./nginx/gen_certificate.sh ./gen_certificate.sh

RUN chmod +x gen_certificate.sh
RUN sh gen_certificate.sh
RUN rm gen_certificate.sh

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 443
