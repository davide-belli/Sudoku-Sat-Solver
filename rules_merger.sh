#!/bin/bash


merge=""

for f in "$@"; do


if [ -f "$f" ]
    then 
        merge+="$(cat "$f")"        
        merge+=$'\n'        
    else (>&2 echo "$f" is not a "file")
fi

done

lines=$(wc -l <<< "$merge")

echo "p cnf 729 $(($lines-1))"
echo "$merge"

