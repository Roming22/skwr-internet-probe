#!/bin/sh

for PACKAGE in black isort pylint; do
    echo "Installing $PACKAGE"
    pip install $PACKAGE
    echo
done