#!/bin/bash

N=100

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
#download the dataset for that difficulty and solve with basic rules
./experiment.sh -n N -d $D

#run the other experiments (modify the code here to use other combinations of strategies)s
./experiment.sh -n 0 -d $D -b -c -a
./experiment.sh -n 0 -d $D -b -l -a
./experiment.sh -n 0 -d $D -p -x
done

mkdir -p ./sudokus/statistics

python statistics.py -d ./sudokus -o ./sudokus/statistics
python statistics2.py -d ./sudokus -o ./sudokus/statistics
python statistics3.py -d ./sudokus -o ./sudokus/statistics
