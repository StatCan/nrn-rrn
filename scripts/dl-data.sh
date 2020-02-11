#!/bin/sh

mkdir -p data/raw/${nrn_pr_code} && 
ogr2ogr -f 'ESRI Shapefile' -t_srs EPSG:4617 data/raw/${nrn_pr_code} /vsizip//vsicurl/${nrn_url}
