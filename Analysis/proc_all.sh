#!/bin/bash
code_files=`find . -name 'coordinate.log'`
root_dir=$PWD

export root_dir

for code_file in $code_files; do
export code_file
bash /data01/SGJ/220128-BL19XU/Scripts/Analysis/proc_in_dir.sh
done
