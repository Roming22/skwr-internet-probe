#!/bin/bash -e
SCRIPT_DIR="$(dirname "$(realpath "$0")")"
SRC_DIR="${SCRIPT_DIR}/k8s"
for MANIFEST in deployments.yml volumes.yml  secrets.yml.secret configmaps.yml.secret namespaces.yml; do
    kubectl delete -f "${SRC_DIR}/${MANIFEST}"
done
