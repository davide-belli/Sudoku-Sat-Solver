#!/bin/bash


merge=""

for f in "$@"; do

    if [ -f "$f" ]
        then
            merge+="$(cat "$f")"
            #merge+=$'\n'
            #(>&2 printf "$f ")
        else (>&2 echo "$f" is not a "file")
    fi
done

#(>&2 printf "\n")


#lines=$(wc -l <<< "$merge")
#echo "p cnf 729 $(($lines-1))"

echo "$merge"

