#!/bin/bash

D=5

N=15

strategies="" #-a -x -c

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -d|--difficulty)
    D="$2"
    shift
    ;;
    -n|--number)
    N="$2"
    shift
    ;;
    -a|--alternative_pairs)
    strategies+='-a '
    ;;
    -c|--cross_hatching)
    strategies+='-c '
    ;;
    -x|--xwing)
    strategies+='-x '
    ;;
esac
shift
done


sudokus="sudokus/$D"

rules="sudokus/rules.cnf"


mkdir -p $sudokus


python web-scraper.py -o $sudokus -d $D -n $N

python rules_generator.py -o $rules $strategies

for s in $sudokus/*_encoded.txt
do
    #echo "$s"
    id=$(basename $s '_encoded.txt')
    echo "$id"
    
    ./rules_merger.sh $rules $s > "$sudokus/${id}_merged.cnf"

    printf "Strategies: $strategies \n\n" >> "$sudokus/${id}_log.txt"
    #./MiniSat_v1.14_linux "$sudokus/${id}_merged.cnf" "$sudokus/${id}_sol.txt" >> "$sudokus/${id}_log.txt"
    minisat -pre "$sudokus/${id}_merged.cnf" "$sudokus/${id}_sol.txt" >> "$sudokus/${id}_log.txt"
    printf "\n\n" >> "$sudokus/${id}_log.txt"
    
    python decode.py -i "$sudokus/${id}_sol.txt" -o "$sudokus/${id}_sol.csv"

done
