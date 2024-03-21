# Stage 1: Build the Angular application
FROM node:20-alpine as builder

WORKDIR /app

# Install Angular CLI and project dependencies
RUN npm install -g @angular/cli@latest

# Copy the app
COPY . .

RUN npm install

# Build the application
RUN npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

RUN apk update && apk upgrade && apk add curl openssl

# Copy the Nginx configuration file
COPY nginx/nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /etc/ssl

COPY ./ssl/* /etc/ssl

COPY --from=builder /app/dist/transcendence/browser /usr/share/nginx/html

# Expose port 443
EXPOSE 443
