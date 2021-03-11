#!/bin/bash -e
ACTION="${1:-apply}"
for MANIFEST in namespaces configmaps secrets volumes deployments; do\
    kubectl "${ACTION}" -f "${MANIFEST}.yml"
done