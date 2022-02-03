#!/bin/bash
code_files=`find . -name 'coordinate.log'`
root_dir=$PWD

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
	for hd5file in $hd5files; do
    		# PREFIX (bash style)
    		prefix=${hd5file%.*}
    		# Log file name
    		logname="$prefix.log"

		if [ ! -e $logname ]; then
			/oys/xtal/cheetah-eiger-zmq/eiger-zmq/bin/cheetah.local $hd5file --nproc=32 --params="cheetah.MinPixCount=4" --params="cheetah.MaxPixCount=30" --params="LocalBGRadius=20" --params="cheetah.MinSNR=3.5" > $logname
		else
			echo "Already processed."
		fi
	done

	cd $wd
	ls heatmap_*.png
	if [ ! -e "heatmap_original.png" ] && [ ! -e "heatmap_threshold.png" ]; then
		echo "Doing Doing"
		python /data01/SGJ/220128-BL19XU/Scripts/Analysis/read_log.py 2
	else
		echo "Plot analysis was finished already."
	fi

# Back to the root directory
cd $root_dir/

fi

echo $wd
done

