#
#url="http://62.12.129.162:4010/data/"
url="http://192.168.91.202/data/"
pre=$1
#num=$2
#dir=$3
dir=$pre"/scan"

cd $dir
pwd
#wget -nd -r -A $pre"_"$num"_*h5" $url
wget -nd -r -A $pre"*h5" $url

exit
