#!/bin/bash

N=50

declare -a diffs=(6)

for D in ${diffs[@]}
do
echo $D 
./experiment.sh -n $N -d $D
#./experiment.sh -n 0 -d $D -x
./experiment.sh -n 0 -d $D -a
./experiment.sh -n 0 -d $D -c
#./experiment.sh -n 0 -d $D -a -c -x

done
