#!/bin/bash
set -e

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
    garage layout assign -z dev -c 1G $NODE_ID
    garage layout apply --version 1

    # Creates buckets
    garage bucket create django-static
    garage bucket create django-media

    # Add an existing key (so it is known ahead of time)
    garage key import --yes -n django GKe8f1ee30bf22a8bc86f0d7a2 f49ac00018a30c5060dc07eeacc156781d21c67d38eadff79b52f393a1c4fd87

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
