#!/bin/bash

if [ $# -eq 1 ]; then
    PROJECT_PATH=$1
else
    echo "ERROR: Please fill the first parameter with path."
    exit 1
fi

chown -R root:bvs $PROJECT_PATH/bire$PROJECT_PATH/
chown -R apache:bvs  $PROJECT_PATH/bire$PROJECT_PATH/media
chown -R apache:bvs  $PROJECT_PATH/bire$PROJECT_PATH/whoosh

find $PROJECT_PATH/bireme -type f | xargs chmod 664
find $PROJECT_PATH/bireme -type d | xargs chmod 775 
