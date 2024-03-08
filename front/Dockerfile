FROM node:alpine AS builder

WORKDIR /usr/src/app

RUN apk update
RUN apk upgrade
RUN apk add curl
RUN npm install -g @angular/cli

COPY . /usr/src/app

RUN npm install

FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY ./nginx/gen_certificate.sh ./gen_certificate.sh

RUN apk update && apk upgrade && apk add openssl curl

RUN chmod +x gen_certificate.sh
RUN sh gen_certificate.sh
RUN rm gen_certificate.sh

COPY --from=builder /usr/src/app/src/ /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 443