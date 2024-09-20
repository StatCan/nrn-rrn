@echo off

rem Activate conda env.
call conda activate nrn-rrn

rem Execute python script.
python conform.py --gui
pause

rem deactivate conda env.
call conda deactivate