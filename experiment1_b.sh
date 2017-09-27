#!/bin/bash

N=5

declare -a diffs=(6 7 8 9)

for D in ${diffs[@]}
do
echo $D

./experiment.sh -d $D -s -l -n $N

done

mkdir -p ./sudokus/statistics

python statistics.py -d ./sudokus -o ./sudokus/statistics