#!/bin/sh

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export nrn_source=`ls /nrn-app/data/raw`

cd $nrn_working_dir
python3 stage_1.py $nrn_source

cd ../stage_2
service postgresql start
python3 stage_2.py $nrn_source
