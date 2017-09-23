#!/bin/bash

N=100

declare -a diffs=(1 2 3 4 5 6 7 8 9)

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