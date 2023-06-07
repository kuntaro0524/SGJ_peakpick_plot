#!/bin/bash
code_files=`find . -name 'coordinate.log'`
root_dir=$PWD

cheetah_path=/oys/xtal/eiger-zmq/cheetah-eiger-zmq/eiger-zmq/bin/
script_path=/home/bladmin/kundev/SGJ/Analysis/

for code_file in $code_files; do
wd=${code_file%/*}

# Find hd5 files
hd5files=`find $wd -name '*master*h5'`

h5_counter=0

for hd5file in $hd5files; do
let h5_counter++
done

# hd5 fileの数を数えている
if [ $h5_counter -eq 0 ]; then
    echo "No .hd5 files in $wd!"
    exit 1
else
    echo "Checking the status of the data processing..."

    # 解析後のログファイルの数を数える
    n_logfiles=`find $wd -name '*master*.log'|wc -l`

    if [ $h5_counter -ne $n_logfiles ]; then
    # Loop to generate 'cheetah log' in the working directory
    # at the same path where the .hd5 files exist

	for hd5file in $hd5files; do
    		# PREFIX (bash style)
    		prefix=${hd5file%.*}
    		# Log file name
    		logname="$prefix.log"
    		# Main loop
		$cheetah_path/cheetah.local $hd5file --nproc=32 --params="cheetah.MinPixCount=4" --params="cheetah.MaxPixCount=30" --params="LocalBGRadius=20" --params="cheetah.MinSNR=3.5" > $logname

	done

	cd $wd
	python $script_path/read_log.py

    else
	    echo "Analysis had been done"
	    echo "Skipping the process"
    fi

# Back to the root directory
cd $root_dir/

fi

echo $wd
done

