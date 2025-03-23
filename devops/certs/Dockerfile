FROM alpine:latest

# Install mkcert dependencies
RUN apk add --no-cache openssl ca-certificates nss-tools

# Install mkcert
RUN wget -O /usr/local/bin/mkcert https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/mkcert-v1.4.4-linux-amd64 && \
    chmod +x /usr/local/bin/mkcert

# Create directory for certificates
WORKDIR /certs

# Script to generate certificates
COPY generate.sh /generate.sh
RUN chmod +x /generate.sh

# Run the certificate generation script
ENTRYPOINT ["/generate.sh"]
