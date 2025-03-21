#!/bin/bash

IMAGE="whisper-worker"
TAG="latest"
echo "src/config/.secrets.yaml" >> .dockerignore
docker buildx build --platform=linux/amd64 -t $IMAGE:$TAG --load -f src/services/whisper_worker/Dockerfile .
# docker push $IMAGE:$TAG
rm .dockerignore  # Reset .dockerignore