#!/bin/bash

N=5

declare -a diffs=(9)

for D in ${diffs[@]}
do
echo $D 
./experiment.sh -n $N -d $D
./experiment.sh -n 0 -d $D -b #--nakedpairs
./experiment.sh -n 0 -d $D -l -c
./experiment.sh -n 0 -d $D -l -c -b 
#./experiment.sh -n 0 -d $D -l -c -b -p -a -x
done
