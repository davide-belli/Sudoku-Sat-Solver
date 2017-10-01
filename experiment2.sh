#!/bin/bash

N=0

difficulty=""

while [[ $# -gt 0 ]]
do
difficulty+="$1 "
shift
done


diffs=($difficulty)

for D in ${diffs[@]}
do
echo $D
./experiment.sh -n 0 -d $D -b -l -x
./experiment.sh -n 0 -d $D -b -c -x
./experiment.sh -n 0 -d $D -b -c -l -x
./experiment.sh -n 0 -d $D -b -c -l -p
./experiment.sh -n 0 -d $D -c -l -x
./experiment.sh -n 0 -d $D -c -p
./experiment.sh -n 0 -d $D -c -x
./experiment.sh -n 0 -d $D -l -p
./experiment.sh -n 0 -d $D -l -x
done

mkdir -p ./sudokus/statistics

python statistics.py -d ./sudokus -o ./sudokus/statistics
