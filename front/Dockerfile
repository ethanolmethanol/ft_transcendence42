FROM node:alpine AS builder

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN npm install -g @angular/cli

RUN npm install

#CMD ["ng", "serve", "--host", "0.0.0.0"]


FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY ./nginx/gen_certificate.sh ./gen_certificate.sh

RUN apk update && apk upgrade && apk add openssl

RUN chmod +x gen_certificate.sh
RUN sh gen_certificate.sh
RUN rm gen_certificate.sh

COPY --from=builder /usr/src/app/src/ /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 443