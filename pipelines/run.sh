#!/bin/sh

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

cd $nrn_working_dir

if [ "$nrn_working_dir" = "/nrn-app/src/stage_1" ]
then
	cp -r /pfs/data/data/raw/. /nrn-app/data/raw
	export nrn_source=`ls /nrn-app/data/raw`
	python3 stage_1.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out
	cp -r /nrn-app/data/raw /pfs/out

elif [ "$nrn_working_dir" = "/nrn-app/src/stage_2" ]
then
	cp /pfs/data/*.gpkg /nrn-app/data/interim
	rm -rf /nrn-app/data/raw
	cp -r /pfs/data/raw /nrn-app/data
	service postgresql start
	export nrn_source=`ls /nrn-app/data/raw`
	python3 stage_2.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out

elif [ "$nrn_working_dir" = "/nrn-app/src/stage_3" ]
then
	cp /pfs/data/*.gpkg /nrn-app/data/interim
	rm -rf /nrn-app/data/raw
	cp -r /pfs/data/raw /nrn-app/data
	export nrn_source=`ls /nrn-app/data/raw`
	python3 stage_3.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out

elif [ "$nrn_working_dir" = "/nrn-app/src/stage_4" ]
then
	cp /pfs/data/*.gpkg /nrn-app/data/interim
	rm -rf /nrn-app/data/raw
	cp -r /pfs/data/raw /nrn-app/data
	export nrn_source=`ls /nrn-app/data/raw`
	python3 stage_4.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out

elif [ "$nrn_working_dir" = "/nrn-app/src/stage_5" ]
then
	cp /pfs/data/*.gpkg /nrn-app/data/interim
	rm -rf /nrn-app/data/raw
	cp -r /pfs/data/raw /nrn-app/data
	export nrn_source=`ls /nrn-app/data/raw`
	python3 stage_5.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out

elif [ "$nrn_working_dir" = "/nrn-app/src/stage_6" ]
then
	cp /pfs/data/*.gpkg /nrn-app/data/interim
	rm -rf /nrn-app/data/raw
	cp -r /pfs/data/raw /nrn-app/data
	export nrn_source=`ls /nrn-app/data/raw`
	python3 stage_6.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out

elif [ "$nrn_working_dir" = "/nrn-app/src/stage_7" ]
then
	cp /pfs/data/*.gpkg /nrn-app/data/interim
	rm -rf /nrn-app/data/raw
	cp -r /pfs/data/raw /nrn-app/data
	export nrn_source=`ls /nrn-app/data/raw`
	python3 stage_7.py $nrn_source
	cp -r /nrn-app/data/interim/. /pfs/out

fi
