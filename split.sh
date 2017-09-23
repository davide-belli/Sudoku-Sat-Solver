#!/bin/bash


out1=""
out2=""

if [[ $# -gt 1 ]]
then
    out1="$1"
    out2="$2"
else
    echo "error!"
    exit
fi

start=false

while read line
do
    if [[ ${line:2} == reading* ]]
    then
        start=true
    fi
    
    
    if [[ ${line:0:2} == 'c ' ]]
    then        
        if $start ; then
            echo "${line:2}" >> "$out2" 
        fi
    else
        echo "${line:2}" >> "$out1"
    fi
done

