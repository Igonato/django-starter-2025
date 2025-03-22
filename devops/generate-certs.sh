#!/bin/bash
# Create directory for certificates
mkdir -p devops/certs

# Generate private key and self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout devops/certs/nginx-selfsigned.key \
  -out devops/certs/nginx-selfsigned.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
  -addext "subjectAltName = DNS:localhost,IP:127.0.0.1"

# Set permissions
chmod 644 devops/certs/nginx-selfsigned.crt
chmod 640 devops/certs/nginx-selfsigned.key

echo "Self-signed certificates generated in devops/certs/"
