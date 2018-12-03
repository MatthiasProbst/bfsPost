#!/bin/bash

# author: Matthias Probst
# date: 2018-11-12

# input arguments: $1=path2resfile
####################################################################
echo $1
if [ $# -eq 0 ];then
   echo "No Solution File given!"
else
    cp quick_view.mcr quick_view_temp.mcr
    bash replacePattern.sh quick_view_temp.mcr RESFILEPATH $1
    /opt/dist/tecplot360ex_2017r2/360ex_2017r2/bin/tec360 -p quick_view_temp.mcr
    echo "Done."  
fi
