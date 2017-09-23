#!/bin/bash

N=100

declare -a diffs=(1 2 3 4 5 6 7 8 9)

for D in ${diffs[@]}
do
echo $D 
./experiment.sh -n $N -d $D
done

mkdir -p ./sudokus/statistics

python statistics.py -d ./sudokus -o ./sudokus/statistics