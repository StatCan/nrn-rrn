#!/bin/sh

# Build the docker image

docker build -t sdi/nrn_fetch -f dockerfiles/FetchData --build-arg nrn_pr_code=nb --build-arg nrn_url=http://geonb.snb.ca/downloads/nbrn/geonb_nbrn-rrnb_shp.zip .

docker build -t sdi/nrn -f dockerfiles/ProcessData --build-arg nrn_working_dir=src/stage_1 .

# Run the docker image

docker run -dit sdi/nrn_fetch

docker run -dit sdi/nrn
