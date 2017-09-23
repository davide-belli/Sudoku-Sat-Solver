#!/bin/bash

N=100

declare -a diffs=(1 2 3 4 5 6 7 8 9)

for D in ${diffs[@]}
do
echo $D
./experiment.sh -n 0 -d $D -b -p
./experiment.sh -n 0 -d $D -b -x
./experiment.sh -n 0 -d $D -b -x -p
./experiment.sh -n 0 -d $D -b -a
done

mkdir -p ./sudokus/statistics

python statistics.py -d ./sudokus -o ./sudokus/statistics