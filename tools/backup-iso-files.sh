#!/bin/bash

NOW=`date +%Y%m%d` 

if [ $# -eq 1 ]; then
    PROJECT_PATH=$1
else
    echo "ERROR: Please fill the first parameter with path."
    exit 1
fi

bkp_dir=$PROJECT_PATH/bkp/
mkdir -p $bkp_dir

cd $PROJECT_PATH/bireme/
tar cvfzp $bkp_dir/iso-files-$NOW.tar.gz media/