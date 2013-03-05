#!/bin/bash

MX=/usr/local/bireme/cisis/5.2b/cisis/mx

if [ $# -eq 1 ]; then
    PROJECT_PATH=$1
else
    echo "ERROR: Please fill the first parameter with path."
    exit 1
fi

$MX iso=$1 -all now