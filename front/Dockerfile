FROM node:alpine

WORKDIR /usr/src/app

RUN apk update
RUN apk upgrade
RUN apk add curl
RUN npm install -g @angular/cli

COPY . /usr/src/app

RUN npm install

CMD ["ng", "serve", "--host", "0.0.0.0"]
