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
./experiment.sh -n 0 -d $D -b
./experiment.sh -n 0 -d $D -l
./experiment.sh -n 0 -d $D -c
./experiment.sh -n 0 -d $D -p
./experiment.sh -n 0 -d $D -x
./experiment.sh -n 0 -d $D -a
done

mkdir -p ./sudokus/statistics

python statistics.py -d ./sudokus -o ./sudokus/statistics