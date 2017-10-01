#!/bin/bash




if [[ $# -eq 3 ]] ; then
    source1="$1"
    source2="$2"
    dest="$3"
else
    echo "usage: ./script.sh <source1> <source2> <dest>"
    exit
fi

mkdir -p "$dest"

cp -r $source1/* $dest/

for d in $source2/*
do

    dn=$(basename $d)
    echo "$d"

    if [ -f $d ]; then
        cat $d >> "$dest/$dn"
    else
        mkdir -p $dest/$dn/

        for f in ${d}/*
        do
            fn=$(basename $f)

            if [ -f $f ]; then
                cat $f >> "$dest/$dn/$fn"
            else
                mkdir -p $dest/$dn/$fn
            fi


        done
    fi
done

