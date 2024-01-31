#!/bin/bash

prefix=$1
wd=$prefix/scan/

cd $wd/
~/kundev/SGJ/Analysis/simple_peaksearch.sh
python ~/kundev/SGJ/Analysis/make_csv_from_scan5.py . 10
