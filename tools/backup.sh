#!/bin/bash

NOW=`date +%Y%m%d` 

if [ $# -eq 1 ]; then
    PROJECT_PATH=$1
else
    echo "ERROR: Please fill the first parameter with path."
    exit 1
fi

source $PROJECT_PATH/submission-env/bin/activate

bkp_dir=$PROJECT_PATH/bkp/
mkdir -p $bkp_dir

cd $PROJECT_PATH/bireme/

python manage.py dumpdata submission > $bkp_dir/submission-$NOW.json
python manage.py dumpdata auth > $bkp_dir/auth-$NOW.json
python manage.py dumpdata center > $bkp_dir/center-$NOW.json
python manage.py dumpdata account.userprofile > $bkp_dir/profile-$NOW.json