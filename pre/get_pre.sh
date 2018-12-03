#!/bin/bash

source ~/.bashrc
# get path to scripts via $PATH
IFS=:
for p in ${PATH}; do
    if [ -f ${p}.bfs_install ]; then
        install_dir=${p}
    fi
done
echo "$install_dir"

casePath=$(pwd)
cp "$install_dir"pre/pre_template.sh $casePath/pre.sh
