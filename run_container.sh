#!/bin/bash

docker run --rm \
 -v `pwd`/envs:/usr/src/app/envs/:ro \
 -v `pwd`/logs:/usr/src/app/logs/:rw \
 --user $(id -u ${USER}):$(id -g ${USER}) \
 --name godaddy_ddns godaddy_ddns:latest $*