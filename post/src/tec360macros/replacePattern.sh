#!/bin/bash

# author: Matthias Probst
# date: 2018-11-12

# replaces pattern in files
# first argument needs to be the filename of file
# second argument needs to be pattern that needs to be replaced
# second argument needs to be the replacement string

FILENAME=$1
PATTERN1=$2
PATTERN2=$3

echo $FILENAME
echo $PATTERN1
echo $PATTERN2

sed -i "s@$PATTERN1@$PATTERN2@g" $FILENAME
