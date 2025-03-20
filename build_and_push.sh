#!/bin/bash

IMAGE="runpod_trigger"
TAG="latest"
echo "src/config/.secrets.yaml" >> .dockerignore
docker buildx build --platform=linux/amd64 -t $IMAGE:$TAG --load -f src/services/runpod_trigger/Dockerfile.base .
# docker push $IMAGE:$TAG
rm .dockerignore  # Reset .dockerignore