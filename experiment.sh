#!/bin/bash

D=5

N=15

Sat4j=false

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
    -4|--sat4j)
    Sat4j=true
    ;;
    *)
    strategies+="$1 "
    ;;
esac
shift
done

echo "Strategies employed: $strategies"


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
        
    if $Sat4j ; then
        > "$sudokus/${id}_sol.txt"
        sat4j "$sudokus/${id}_merged.cnf" | ./split.sh "$sudokus/${id}_sol.txt" "$sudokus/${id}_log.txt"
    else
        #./MiniSat_v1.14_linux "$sudokus/${id}_merged.cnf" "$sudokus/${id}_sol.txt" >> "$sudokus/${id}_log.txt"
        minisat -pre "$sudokus/${id}_merged.cnf" "$sudokus/${id}_sol.txt" >> "$sudokus/${id}_log.txt"
    fi
    
    printf "\n\n" >> "$sudokus/${id}_log.txt"
    
    python decode.py -i "$sudokus/${id}_sol.txt" -o "$sudokus/${id}_sol.csv"

done
