#!/bin/bash

originx=1136 
originy=1027

let startx=$originx-10
let endx=$originx+10

let starty=$originy-10
let endy=$originy+10

rootdir=`pwd`
for i in `seq $startx 2 $endx`; do
	for j in `seq $starty 2 $endy`; do
		wd=${i}_${j}
		mkdir $wd/
		cd $wd/
		cat ../XDS.INP.TEMPLATE > XDS.INP
		echo "ORGX=$i ORGY=$j" >> XDS.INP
		\rm -rF "IDXREF.LP"
		xds_par 
		#if [ -e "IDXREF.LP" ]; then
			#grep "UNIT CELL PARAMETERS" IDXREF.LP
			#set idxref_result=`grep "UNIT CELL PARAMETERS" IDXREF.LP`
			#echo "EEEEEEEEEEEEEEEEE=" $idxref_result
			#echo $i $j $idxref_result >> result.log
		#else
			#echo $i $j "Failed in indexing"
		#fi
		cd $rootdir
	done
done
