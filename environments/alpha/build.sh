#!/bin/bash
set -e

echo "Building Docker image: ${DOCKER_IMAGE} with PORT ${PORT}"

if [ -n "${CACHE_FROM}" ]; then
  echo "Using cache from: ${CACHE_FROM}"
  docker buildx build --build-arg PORT=${PORT} --cache-from="type=local,src=${CACHE_FROM}" --cache-to="type=local,dest=${CACHE_FROM}" -t "${DOCKER_IMAGE}" -f ./environments/alpha/Dockerfile . --push
else
  docker build --build-arg PORT=${PORT} -t "${DOCKER_IMAGE}" -f ./environments/alpha/Dockerfile .
  echo "Pushing Docker image: ${DOCKER_IMAGE}"
  docker push "${DOCKER_IMAGE}"
fi
