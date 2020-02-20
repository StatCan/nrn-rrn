#!/bin/sh

docker-compose up --build

docker cp "$(docker-compose ps -q nrn)":/nrn-app/data/interim/nb.gpkg /tmp
