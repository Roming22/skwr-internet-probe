# Template for a [SKWR](https://github.com/Roming22/skwr) module

## image/

* `Dockerfile`: Used to create the container image.
* `module`: This folder shoud contain a `bin` directory with a `run.sh` script that starts the service to be run by the container. Any static data should be under this directory as well.
* `module/bin/run.sh`: Default entrypoint.
* `module/bin/healthcheck.sh`: Default health check.

## etc/

This directory holds the configuration of the systemd service as well as some of the docker options to be used when starting the container.

### service.cfg

* `DESCRIPTION`: The description of the systemd service.
* `DOCKER_NETWORK`: By default each container is on its own network to isolate it. If multiple containers need to be connected together, set the DOCKER_NETWORK to a common value.
* `DOCKER_OPTIONS`: Additional docker options.

### *.env

Any `*.env` file in this directory will be automatically loaded when the container is started.


## volumes/

* `config`: Configuration of the volumes to be mounted in the container. The format is `source/path/from/volumes:/target/path/in/container[:ro]`.
