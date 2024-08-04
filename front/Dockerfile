# hadolint global ignore=DL3018
# Stage 1: Build the Angular application
FROM node:20-alpine as builder
WORKDIR /app
# Install Angular CLI and project dependencies
RUN npm install -g @angular/cli@latest
# Copy the app
COPY . .

RUN npm install && \
	# npm update && \
# Build the application
	npm run build

# Stage 2: Serve the application with Nginx
FROM nginx:1.25.4-alpine

WORKDIR /

RUN apk update && apk upgrade && apk add --no-cache 'curl' 'openssl'

# Copy the Nginx configuration file
COPY nginx/nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /etc/ssl
COPY ./ssl/* /etc/ssl
COPY --from=builder /app/dist/transcendence/browser /usr/share/nginx/html
# Expose port 443
EXPOSE 443
