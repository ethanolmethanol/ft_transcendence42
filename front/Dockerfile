# Stage 1: Build the Angular application
FROM node:20-alpine as builder

WORKDIR /app

# Install Angular CLI and project dependencies
RUN npm install -g @angular/cli@latest
RUN npm install --save-dev @angular-devkit/build-angular@latest
RUN npm install rollup

# Copy package.json and package-lock.json
COPY . .

RUN rm package-lock.json

RUN npm install
RUN npm update

# Build the application
RUN ng build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

RUN apk update && apk upgrade && apk add curl openssl

# Copy the Nginx configuration file
COPY nginx/nginx.conf /etc/nginx/nginx.conf

COPY nginx/gen_certificate.sh .

RUN chmod +x ./gen_certificate.sh
RUN ./gen_certificate.sh
RUN rm ./gen_certificate.sh

COPY --from=builder /app/dist/transcendence/browser /usr/share/nginx/html

# Expose port 443
EXPOSE 443
