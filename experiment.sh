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


strategy_arr=($strategies)

strategies="${strategies// }"

sudokus="sudokus/$D"

rules_dir="sudokus/rules"

mkdir -p "$rules_dir"

mkdir -p "$sudokus/statistics/"


rules_files=""

for s in ${strategy_arr[@]}
do
    echo $s
    rules_files+="$rules_dir/$s.cnf "
    if [ ! -f "$rules_dir/$s.cnf" ]; then
        python rules_generator.py -o "$rules_dir/$s.cnf" $s
    fi
done

rules="$rules_dir/$strategies.cnf"

echo "$rules"

if [ ! -f $rules ]; then
    ./rules_merger.sh $rules_files > "$rules"
fi



len_rules=$(wc -l < "$rules")

echo $len_rules

python web-scraper.py -o $sudokus -d $D -n $N


for s in $sudokus/*_encoded.txt
do
    #echo "$s"
    id=$(basename $s '_encoded.txt')
    echo "$id"

    len_sudoku=$(wc -l < "$s")

    printf "p cnf 729 $(($len_sudoku + $len_rules -1))\n" > "$sudokus/${id}_${strategies}_merged.cnf"
    ./rules_merger.sh $rules $s >> "$sudokus/${id}_${strategies}_merged.cnf"

    printf "Strategies: $strategies \n\n" >> "$sudokus/${id}_log.txt"
        
    if $Sat4j ; then
        > "$sudokus/${id}_sol.txt"
        sat4j "$sudokus/${id}_${strategies}_merged.cnf" | ./split.sh "$sudokus/${id}_sol.txt" "$sudokus/${id}_log.txt"
    else
        #./MiniSat_v1.14_linux "$sudokus/${id}_${strategies}_merged.cnf" "$sudokus/${id}_sol.txt" >> "$sudokus/${id}_log.txt"
        minisat -pre -rnd-freq=0 "$sudokus/${id}_${strategies}_merged.cnf" "$sudokus/${id}_sol.txt" >> "$sudokus/${id}_log.txt"
    fi

    rm "$sudokus/${id}_${strategies}_merged.cnf"
    printf "\n\n" >> "$sudokus/${id}_log.txt"
    
    python decode.py -i "$sudokus/${id}_sol.txt" -o "$sudokus/${id}_sol.csv"

done


#python single_statistics.py -d "$sudokus" -o "$sudokus/statistics"