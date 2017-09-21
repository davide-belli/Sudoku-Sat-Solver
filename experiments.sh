#!/bin/bash

N=10

declare -a diffs=(7)

for D in ${diffs[@]}
do
echo $D 
./experiment.sh -n $N -d $D
#./experiment.sh -n 0 -d $D -l
./experiment.sh -n 0 -d $D -x
./experiment.sh -n 0 -d $D -l -c
./experiment.sh -n 0 -d $D -l -c -x
done
