#!/bin/bash

N=30

declare -a diffs=(7)

for D in ${diffs[@]}
do
echo $D 
./experiment.sh -n $N -d $D
./experiment.sh -n 0 -d $D -b
./experiment.sh -n 0 -d $D -l -c
./experiment.sh -n 0 -d $D -l -c -b 
./experiment.sh -n 0 -d $D -l -c -b -p
done
