#!/bin/bash

start_date=`date`
n_cycle=1
root_dir=$PWD

while true
do
	code_files=`find . -name 'coordinate.log'`
	export root_dir

	for code_file in $code_files; do
		export code_file
		bash /data01/SGJ/220128-BL19XU/Scripts/Analysis/proc_in_dir.sh
	done
let ++n_cycle
	echo "Started: $start_date Cycle= $n_cycle"
	echo "waiting for the next cycle..."
sleep 60

done
