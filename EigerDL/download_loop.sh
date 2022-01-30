#
if [ $# != 2 ]; then
    echo "Syntax error!"
    echo "Usage: download_loop.sh prefix nCycle"
    exit 1
fi

#url="http://62.12.129.162:4010/data/"
url="http://192.168.91.202/data/"
pre=$1
#num=$2
#dir=$3
cycle=$2
dir=$pre"/scan"

cd $dir
pwd

ii=0
while [ "$ii" -lt "$cycle" ]
do
#wget -nd -r -A $pre"_"$num"_*h5" $url
wget -nd -r -A $pre"*h5" $url

let ii++
done
exit
