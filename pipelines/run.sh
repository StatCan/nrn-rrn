#!/bin/sh

export nrn_source=`ls /pfs/input/`

cd $nrn_working_dir

if [ "$nrn_working_dir" == "src/stage_1" ]
then
	cp -r /pfs/input/. ../../data/raw	
	python3 stage_1.py $nrn_source

elif [ "$nrn_working_dir" == "src/stage_2" ]
then
	python3 stage_2.py $nrn_source
	cp -r ../../data/interim/$nrn_source.gpkg /pfs/output/	
fi
