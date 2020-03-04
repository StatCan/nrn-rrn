#!/bin/sh

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export nrn_source=`ls /pfs/data/data/raw`

cd $nrn_working_dir

if [ "$nrn_working_dir" = "/nrn-app/src/stage_1" ]
then
	cp -r /pfs/data/data/raw/$nrn_source /nrn-app/data/raw
	python3 stage_1.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out/data/
	mkdir -p /pfs/out/data/raw
	cp -r /nrn-app/data/raw/. /pfs/out/data/raw/

elif [ "$nrn_working_dir" = "/nrn-app/src/stage_2" ]
then
	cp /pfs/data/data/*.gpkg /nrn-app/data/interim
	service postgresql start
	python3 stage_2.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out/data/
elif [ "$nrn_working_dir" = "/nrn-app/src/stage_3" ]
then
	cp /pfs/data/data/*.gpkg /nrn-app/data/interim
	python3 stage_3.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out/data/
elif [ "$nrn_working_dir" = "/nrn-app/src/stage_4" ]
then
	cp /pfs/data/data/*.gpkg /nrn-app/data/interim
	python3 stage_4.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out/data/
elif [ "$nrn_working_dir" = "/nrn-app/src/stage_5" ]
then
	cp /pfs/data/data/*.gpkg /nrn-app/data/interim
	python3 stage_5.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out/data/
elif [ "$nrn_working_dir" = "/nrn-app/src/stage_6" ]
then
	cp /pfs/data/data/*.gpkg /nrn-app/data/interim
	python3 stage_6.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out/data/
elif [ "$nrn_working_dir" = "/nrn-app/src/stage_7" ]
then
	cp /pfs/data/data/*.gpkg /nrn-app/data/interim
	python3 stage_7.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out/data/
fi
