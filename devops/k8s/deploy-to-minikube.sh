#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"
if [[ -z "${PROJECT_NAME}" ]]; then
    PROJECT_NAME=$(basename "$PROJECT_DIR")
fi

if [[ -z "${PROJECT_HOST}" ]]; then
    PROJECT_HOST=$(echo "$PROJECT_NAME.internal")
fi

# Check if minikube is running
if ! minikube status | grep -q "Running"; then
    echo "Minikube is not running. Starting minikube..."
    minikube start
fi

# Check if minikube ingress addon is enabled
if ! minikube addons list | grep -E "ingress.*enabled" > /dev/null; then
    echo "Minikube ingress addon is not enabled. Enabling..."
    minikube addons enable ingress
    minikube addons enable ingress-dns
fi

echo
echo "Building Docker image inside minikube..."
eval $(minikube docker-env)
docker build -t "$PROJECT_NAME-web:latest" "$PROJECT_DIR"
docker build -t "$PROJECT_NAME-s3:latest" -f "$PROJECT_DIR/devops/s3/Dockerfile" "$PROJECT_DIR"


cd $PROJECT_DIR

echo
echo "Rendering Kubernetes manifests..."
rm -rf devops/k8s/minikube
cp -r devops/k8s/templates devops/k8s/minikube
sed -i 's/__PROJECT_NAME__/'"$PROJECT_NAME"'/g' \
    devops/k8s/minikube/*
sed -i 's/__WEB_SERVICE_IMAGE__/'"$PROJECT_NAME-web:latest"'/g' \
    devops/k8s/minikube/*
sed -i 's/__S3_SERVICE_IMAGE__/'"$PROJECT_NAME-s3:latest"'/g' \
    devops/k8s/minikube/*
sed -i 's/__DJANGO_SECRET_KEY__/'"$SECRET_KEY"'/g' \
    devops/k8s/minikube/*
sed -i 's/__PROJECT_HOST__/'"$PROJECT_HOST"'/g' \
    devops/k8s/minikube/*

echo
echo "Deploying to minikube..."
# Create the namespace if needed
if ! kubectl get namespace "$PROJECT_NAME" >/dev/null 2>&1; then
    echo "Creating namespace..."
    kubectl create namespace "$PROJECT_NAME"
fi

if kubectl get secret web-secrets --namespace="$PROJECT_NAME" >/dev/null 2>&1; then
  echo "Secrets already exists. Skipping..."
else
  echo "Creating secrets..."
  kubectl create secret generic web-secrets \
    --namespace="$PROJECT_NAME" \
    --from-literal="SECRET_KEY=$(openssl rand -hex 32)" \
    --from-literal="S3_ACCESS_KEY_ID=GK$(openssl rand -hex 12)" \
    --from-literal="S3_SECRET_ACCESS_KEY=$(openssl rand -hex 32)"
fi

if command -v mkcert >/dev/null 2>&1; then
    echo "Generating TLS certificates..."

    # Temporary directory for certificates
    CERT_DIR=$(mktemp -d)
    trap "rm -rf $CERT_DIR" EXIT

    mkcert -cert-file "$CERT_DIR/tls.crt" -key-file "$CERT_DIR/tls.key" "$PROJECT_HOST"

    if kubectl get secret "$PROJECT_NAME-cert" --namespace="$PROJECT_NAME" >/dev/null 2>&1; then
        echo "TLS secret already exists. Updating..."
        kubectl delete secret "$PROJECT_NAME-cert" --namespace="$PROJECT_NAME"
    fi

    echo "Creating certificate secret..."
    kubectl create secret tls "$PROJECT_NAME-cert" \
        --cert="$CERT_DIR/tls.crt" \
        --key="$CERT_DIR/tls.key" \
        --namespace="$PROJECT_NAME"

    sed -i 's/__TLS_SECRET_NAME__/'"$PROJECT_NAME-cert"'/g' devops/k8s/minikube/*
else
    echo "Skipping certificate generation... (mkcert not found)"
    echo "Install mkcert (https://github.com/FiloSottile/mkcert)"
    echo "to automatically generate valid local HTTPS certificates."
    sed -i '/# TLS_SECTION_START/,/# TLS_SECTION_END/d' devops/k8s/minikube/*
fi

# Ensure that migrate and collectstatic jobs will rerun
# In produciton you can tie this to app version... Or leave it as-is
kubectl delete job "$PROJECT_NAME-migrate-job" -n "$PROJECT_NAME" --ignore-not-found=true
kubectl delete job "$PROJECT_NAME-collectstatic-job" -n "$PROJECT_NAME" --ignore-not-found=true

echo "Applying manifests..."
kubectl apply -Rf devops/k8s/minikube -n "$PROJECT_NAME"

echo
echo "Waiting for services to be ready..."
kubectl wait --for=condition=ready pod -l service="web" -n "$PROJECT_NAME" --timeout=60s

echo
echo "Your application should be accessible at https://$PROJECT_HOST"
echo "You may need to run \"minikube tunnel\" and update your system hosts file"
echo "See the Kubernetes section of the README.md for details"
