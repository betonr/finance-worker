#!/bin/bash

##### DEPLOY

echo
echo "BUILD STARTED"
echo

echo
echo "NEW TAG - API:"
read API_TAG

IMAGE_API="betonoronha/homol:worker-finance"

IMAGE_API_FULL="${IMAGE_API}-v${API_TAG}"

docker build -t ${IMAGE_API_FULL} -f docker/Dockerfile .

docker push ${IMAGE_API_FULL}
