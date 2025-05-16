#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"
PROJECT_NAME=$(basename "$PROJECT_DIR")

# Check if minikube is running
if ! minikube status | grep -q "Running"; then
    echo "Minikube is not running. Starting minikube..."
    minikube start
fi

# Build the Docker image inside minikube
echo "Building Docker image inside minikube..."
eval $(minikube docker-env)
docker build -t "$PROJECT_NAME-web:latest" "$PROJECT_DIR"

rm -rf devops/k8s/minikube
cp -r devops/k8s/templates devops/k8s/minikube

sed -i 's/WEB_SERVICE_IMAGE/'"$PROJECT_NAME-web:latest"'/g' devops/k8s/minikube/*.yaml
