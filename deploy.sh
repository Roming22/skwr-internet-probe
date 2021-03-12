#!/bin/bash -e
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
SRC_DIR="${SCRIPT_DIR}/k8s"
for MANIFEST in namespaces.yml configmaps.yml.secret secrets.yml.secret volumes.yml deployments.yml; do\
    kubectl apply -f "${SRC_DIR}/${MANIFEST}"
done
