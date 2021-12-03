#!/bin/bash

filelist=`ls *master*h5`

#echo $filelist

for eachfile in $filelist; do
prefix=${eachfile%.*} 
logname=$prefix.log
echo "Writing" $logname

#/oys/xtal/cheetah-eiger-zmq/eiger-zmq/bin/cheetah.local $eachfile > $logname
/oys/xtal/cheetah-eiger-zmq/eiger-zmq/bin/cheetah.local $eachfile  --params="cheetah.MinPixCount=4" --params="cheetah.MaxPixCount=20" --params="cheetah.MinSNR=1.9" > $logname

done

python /data01/SGJ/211127-BL19XU/Scripts/read_log.py
