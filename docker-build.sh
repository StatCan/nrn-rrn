#!/bin/sh

# Build the docker image

docker build -t sdi/nrn .

# Run the docker image

docker run -dit sdi/nrn
