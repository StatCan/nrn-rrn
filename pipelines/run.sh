#!/bin/sh

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

ls /pfs/out/data/raw
export nrn_source=`ls /pfs/out/data/raw`

cd $nrn_working_dir

if [ "$nrn_working_dir" = "/nrn-app/src/stage_1" ]
then
	cp -r /pfs/out/data /nrn-app/data
	python3 stage_1.py $nrn_source
	cp -r /nrn-app/data /pfs/out/data

elif [ "$nrn_working_dir" = "/nrn-app/src/stage_2" ]
then
	python3 stage_2.py $nrn_source
fi
