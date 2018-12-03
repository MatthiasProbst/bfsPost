#!/bin/bash

casePath=$(pwd) # case path is currend directory

# get path to scripts via $PATH
IFS=:
for p in ${PATH}; do
    if [ -f ${p}.bfs_install ]; then
        install_dir=${p}
    fi
done
echo $install_dir
postpath="$install_dir"post/src


if echo $casePath | grep -q "pocket";then
    geomtype=pocket
elif echo $casePath | grep -q "ercoftac"; then
    geomtype=classic
fi
echo $geomtype

latestResFile=$(ls -t *.res | head -1) # latest res-file
caseName=${latestResFile::-4} # cur string ".res"

if [[ "$1" == "-info" ]]; then
  while read line
    do
      echo "$line"
    done < $caseInfo
elif [[ "$1" == "-p" ]]; then
    python3 "$postpath"/py/plot_U_profiles.py -n $caseName -s "$casePath" -v cfx -g $geomtype
elif [[ "$1" == "-qv" ]]; then
    cd "$postpath"/tec360macros/
    bash "$postpath"/tec360macros/quick_view.sh "$casePath"/"$latestResFile"
    cd "$casePath"
else
    subCasePath="$casePath"/"$caseName"
    echo "$latestResFile"
    if ! [ -d "$casePath"/post ]; then
        mkdir "$casePath"/post
    fi
    cd "$postpath"/tec360macros/
    bash extractVelProfiles2.sh "$casePath"/"$latestResFile" "$casePath"/post "$casePath"/slice laminar
    bash extractTauX.sh "$casePath"/"$latestResFile" "$casePath"/post laminar
    cd "$casePath"
    python3 "$postpath"/py/plot_U_profiles.py -n $caseName -s "$casePath" -v cfx -g $geomtype
fi
