#!/bin/bash

IFS=:

for p in ${PATH}; do
    if [ -f ${p}.bfs_install ]; then
        install_dir=${p}
    fi
done

echo $install_dir
