#!/bin/bash

# author: Matthias Probst
# date: 2018-11-12
# extracts velocity profiles from tecplot

# input arguments: $1=path2resfile
####################################################################

if [ $# -eq 1 ];then
   echo "No Solution File given!"
else
    if [ $3 == turbulent ]; then
        cp taux_Turbulent.mcr taux_temp.mcr
    elif [ $3 == laminar ]; then
        cp taux_Laminar.mcr taux_temp.mcr
    fi
    echo $3
    
    bash replacePattern.sh taux_temp.mcr CSVFILENAMEPATH $2
    bash replacePattern.sh taux_temp.mcr CSVFILENAME taux
    bash replacePattern.sh taux_temp.mcr RESFILEPATH $1            
            
    /opt/dist/tecplot360ex_2017r2/360ex_2017r2/bin/tec360 -b -p taux_temp.mcr
    echo "Done."  
    
    rm taux_temp.mcr
fi
