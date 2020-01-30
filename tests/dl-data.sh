#!/bin/sh

mkdir -p data/raw/nb && 
ogr2ogr -f 'ESRI Shapefile' data/raw/nb/geonb_nbrn-rrnb_shp '/vsizip//vsicurl/http://geonb.snb.ca/downloads/nbrn/geonb_nbrn-rrnb_shp.zip'
