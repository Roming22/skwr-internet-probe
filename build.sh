#!/bin/bash -e
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
SRC_DIR="${SCRIPT_DIR}/images"
REPOSITORY="k3d-registry.localhost:5000"
for DOCKERFILE in $(find "${SRC_DIR}" -name Dockerfile -type f); do
    IMAGE_DIR="$(dirname "${DOCKERFILE}")"
    IMAGE_NAME="$(realpath "${IMAGE_DIR}" --relative-to="${SRC_DIR}")"
    IMAGE="${REPOSITORY}/${IMAGE_NAME}:latest"
    docker build -t "${IMAGE}" "${IMAGE_DIR}"
    docker push "${IMAGE}"
done

