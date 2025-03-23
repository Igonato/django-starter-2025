#!/bin/sh
set -e

if [ -f /certs/selfsigned.crt ] && [ -f /certs/selfsigned.key ]; then
    echo "Certificates already exist in /certs directory."
    echo "To regenerate certificates, delete the existing files."

    exit 0
fi

# Create a temporary directory for mkcert files
CAROOT=/tmp/mkcert
export CAROOT

# Create CA
echo "Creating local CA..."
mkcert -install

# Generate certificate
echo "Generating certificates for localhost and 127.0.0.1..."
mkcert \
    -cert-file /certs/selfsigned.crt \
    -key-file /certs/selfsigned.key \
    localhost 127.0.0.1

# Copy CA certificate for users to install
cp "$CAROOT/rootCA.pem" /certs/

echo "Certificate generation complete!"
echo ""
echo "To trust this certificate:"
echo "1. Open browser settings and search for 'certificates'"
echo "2. Click 'Manage certificates' and go to 'Authorities' tab"
echo "3. Click 'Import' and select the devops/certs/rootCA.pem file"
echo "4. Check 'Trust this certificate for identifying websites'"
echo "5. Click OK and restart your browser"
