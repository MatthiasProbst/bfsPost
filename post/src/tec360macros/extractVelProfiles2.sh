#!/bin/bash

# author: Matthias Probst
# date: 2018-11-12
# extracts velocity profiles from tecplot

# input arguments: $1=path2resfile $2=CSVFILENAMEPATH $3=path2sliceFile $4=lamianr/turbulent
####################################################################

if [ $# -eq 1 ];then
   echo "No Solution File given!"
else

    # read xH Y1POS and Y2POS from file
    while IFS=, read -r xH Y1POS Y2POS; do
    
        if [ "$xH" != "#x/h" ]; then
    
            XPOS=$(echo "$xH*0.025" | bc)
            echo x="$XPOS", x/H="$xH", Y1="$Y1POS", Y2="$Y2POS"
        
            # copy original macro to temporary macro
            if [ $4 == turbulent ]; then
                cp extractVelProfiles_Turbulent.mcr extractVelProfiles_XH"$xH"_temp.mcr
            elif [ $4 == laminar ]; then
                cp extractVelProfiles_Laminar.mcr extractVelProfiles_XH"$xH"_temp.mcr
            fi

            # replace pattern
            zero=0
            if (( $(echo "$XPOS*10 <= $zero" | bc -l) )); then
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr CSVFILENAMEPATH $2
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr CSVFILENAME XH"$xH"
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr X1POS $XPOS
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr Y1POS $Y1POS
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr X2POS $XPOS
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr Y2POS $Y2POS
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr RESFILEPATH $1
            else
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr CSVFILENAMEPATH $2
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr CSVFILENAME XH"$xH"
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr X1POS $XPOS
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr Y1POS $Y1POS
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr X2POS $XPOS
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr Y2POS $Y2POS
                bash replacePattern.sh extractVelProfiles_XH"$xH"_temp.mcr RESFILEPATH $1
            fi

            # execure via tecplot (console)
            /opt/dist/tecplot360ex_2017r2/360ex_2017r2/bin/tec360 -b -p extractVelProfiles_XH"$xH"_temp.mcr
            #/opt/dist/tecplot360ex_2017r2/360ex_2017r2/bin/tec360 -p extractVelProfiles_temp.mcr

            # delete temporary macro again
            #if [ $5 == -r ]; then
            #    rm extractVelProfiles_XH"$xH"_temp.mcr
            #fi

        fi
        
    done < $3
    echo "Done."  
fi
