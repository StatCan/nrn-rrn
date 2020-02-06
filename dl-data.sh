#!/bin/sh

mkdir -p data/raw/${nrn_source} && 
ogr2ogr -f 'ESRI Shapefile' data/raw/${nrn_source} /vsizip//vsicurl/${nrn_url}
