#!/bin/bash
set -e

cd /etc
cp garage-config-template.toml garage.toml
sed -i 's/__GARAGE_REPLICATION_FACTOR__/'"${GARAGE_REPLICATION_FACTOR:-1}"'/g' garage.toml
sed -i 's/__GARAGE_RPC_SECRET__/'"${GARAGE_RPC_SECRET:-0000000000000000000000000000000000000000000000000000000000000000}"'/g' garage.toml
sed -i 's/__GARAGE_S3_REGION_NAME__/'"${S3_REGION_NAME:-garage}"'/g' garage.toml
sed -i 's/__GARAGE_ADMIN_TOKEN__/'"${GARAGE_ADMIN_TOKEN:-garage-admin-token-local-dev-only}"'/g' garage.toml
sed -i 's/__GARAGE_METRICS_TOKEN__/'"${GARAGE_METRICS_TOKEN:-garage-metrics-token-local-dev-only}"'/g' garage.toml

# Start Garage in the background
garage server &
GARAGE_PID=$!

# Wait for Garage to be ready
/wait-for-it.sh 0.0.0.0:3900 --timeout=30

# Get the node ID
NODE_ID=$(garage status | grep "NO ROLE ASSIGNED" | awk '{print $1}')

if [ -n "$NODE_ID" ]; then
    echo "Found uninitialized node: $NODE_ID"

    # Setup the node
    garage layout assign -z dev -c ${GARAGE_INIT_SIZE:-1G} $NODE_ID
    garage layout apply --version 1

    # Creates buckets
    garage bucket create django-static
    garage bucket create django-media

    # Add an existing key (simplifies setup since it is known ahead of time)
    garage key import --yes -n django $S3_ACCESS_KEY_ID $S3_SECRET_ACCESS_KEY

    # Change the permissions
    garage bucket allow \
      --read \
      --write \
      --owner \
      django-static \
      --key django

    garage bucket allow \
      --read \
      --write \
      --owner \
      django-media \
      --key django

    # Enable public access
    garage bucket website --allow django-static
    garage bucket website --allow django-media

    echo "🧺 Garage initialization complete! ✨"
else
    echo "🧺 Garage node already initialized, skipping the setup..."
fi

# Keep the script running with the Garage server process
wait $GARAGE_PID
