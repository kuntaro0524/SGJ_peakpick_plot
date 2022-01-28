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

echo $h5_counter Exists!

if [ $h5_counter -eq 0 ]; then
    echo "No files!"
else
    echo "Process will start!"
    # PREFIX
    prefix=${hd5file%.*}
    # Log file name
    logname="$PREFIX.log"

    echo "Process has started $hd5file"
/oys/xtal/cheetah-eiger-zmq/eiger-zmq/bin/cheetah.local $hd5file --nproc=32 --params="cheetah.MinPixCount=4" --params="cheetah.MaxPixCount=30" --params="LocalBGRadius=20" --params="cheetah.MinSNR=3.5" > $logname
    cd $wd
python /data01/SGJ/211127-BL19XU/Scripts/Analysis/read_log.py
# Back to the root directory
cd $root_dir/

fi

echo $wd
done
