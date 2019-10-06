#!/bin/bash

# You may want to add some configuration/init steps here

# Let SKWR know that the container is up and running 
echo "[`hostname -s`] Started"

# Overwrite this section
while true; do
	echo "I'm alive"
	sleep 10
done
