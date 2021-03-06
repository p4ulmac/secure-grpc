#!/bin/bash

if [ -z "${VIRTUAL_ENV}" ] ; then
    echo "Must run from Python virtual environment"
    exit 1
fi
SECURE_GRPC_PATH="${VIRTUAL_ENV}/.."

# For pass-though of --authentication and --signer options
more_options="$@"

# Remove the client docker container from the previous run if it is still around
docker rm adder-client-host >/dev/null 2>&1

# Start the client docker container
docker run \
    --name adder-client-host \
    --network secure-grpc-net \
    --ip 172.30.0.3 \
    --hostname adder-client-host \
    --volume ${SECURE_GRPC_PATH}:/host \
    secure-grpc \
    bash -c "cd /host && python3 client.py --server-host adder-server-host ${more_options}"
