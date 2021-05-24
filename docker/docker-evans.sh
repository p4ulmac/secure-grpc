#!/bin/bash

if [ -z "${VIRTUAL_ENV}" ] ; then
    echo "Must run from Python virtual environment"
    exit 1
fi
SECURE_GRPC_PATH="${VIRTUAL_ENV}/.."

# For pass-though of authentication-related command-line options
more_options="$@"

# Remove the Evans client docker container from the previous run if it is still around
docker rm secure-grpc-client >/dev/null 2>&1

# Start the Evans client docker container
docker run \
    --name secure-grpc-client \
    --network secure-grpc-net \
    --ip 172.30.0.3 \
    --hostname secure-grpc-client \
    --volume ${SECURE_GRPC_PATH}:/host \
    secure-grpc \
    bash -c "echo ./evans --proto /host/adder.proto cli call --host secure-grpc-server \
             ${more_options}"
