#!/bin/bash

if [[ $1 == -clean ]];then
    rm *.ires
    rm *.res*
    rm *.out
    rm -r post
    rm -r def_file_*
fi

casedir=$(pwd)
casename=${PWD##*/}

# get path to scripts via $PATH
IFS=:
for p in ${PATH}; do
    if [ -f ${p}.bfs_install ]; then
        install_dir=${p}
    fi
done
echo "$install_dir"

Re=1000
mesh_file="$install_dir"mesh/500_pocket/laminar/"$casename"/mesh.cfx5
ccl_file="$install_dir"cfx/500_pocket/laminar/500_pocket_laminar.ccl

geom_file="$install_dir"cfx/500_pocket/laminar/geomprop
matprop_file="$install_dir"cfx/500_pocket/laminar/matprop
slice_file="$install_dir"cfx/500_pocket/laminar/slice

# create laminar flow profile
python "$install_dir"pre/create_laminar_flow_profile.py -r $Re -p full -o $casedir/inlet_flow_profile.csv

# copy ccl file to case dir
cp $ccl_file "$casedir"/ccl_file.ccl

# set velocity profile path in ccl_file:
bash "$install_dir"post/src/tec360macros/replacePattern.sh ccl_file.ccl INLETVELOCITYPROFILE_PATH $casedir/inlet_flow_profile.csv

# create def-file:
echo "preparing run..."
cfx5gtmconv -overwrite -icem "$mesh_file" -def def_file.def -ccl "$casedir"/ccl_file.ccl

# solve problem:
echo "solving..."
cfx5solve -batch -def def_file.def -par-local -partition 2
