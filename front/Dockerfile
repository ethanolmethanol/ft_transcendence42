FROM node:alpine AS builder

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN npm install -g @angular/cli

RUN npm install

#CMD ["ng", "serve", "--host", "0.0.0.0"]



FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /usr/src/app/src/ /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 443