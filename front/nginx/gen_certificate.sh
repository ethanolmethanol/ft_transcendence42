#!/bin/sh

# Define certificate details
COUNTRY="FR"
STATE="Parid"
LOCALITY="Paris"
ORGANIZATION="42"
ORGANIZATIONAL_UNIT="Your Unit"
COMMON_NAME="localhost"
EMAIL="your.email@example.com"

cd /etc/ssl

# Generate a private key
openssl genrsa -out server.key 2048

# Create a self-signed certificate
openssl req -new -x509 -sha256 -key server.key -out server.crt -days 365 -subj "/C=$COUNTRY/ST=$STATE/L=$LOCALITY/O=$ORGANIZATION/OU=$ORGANIZATIONAL_UNIT/CN=$COMMON_NAME/emailAddress=$EMAIL"

# Verify the certificate
openssl x509 -in server.crt -text -noout
echo "Certificate created"