#!/bin/sh

service postgresql start && 
psql -f /nrn-app/tests/psql-test.sql && 
ogr2ogr -f "PostgreSQL" PG:"host='localhost' dbname='gisdb' port='5432' user='postgres' password='password'" '/vsizip//vsicurl/https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/physical/ne_110m_land.zip' -nln natearth -nlt PROMOTE_TO_MULTI &&
mkdir -p tests/natearth && 
ogr2ogr -f "ESRI Shapefile" tests/natearth/test.shp PG:"host='localhost' user='postgres' dbname='gisdb' password='password'" -sql "SELECT * FROM natearth WHERE scalerank = 0"
