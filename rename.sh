#!/usr/bin/env bash

r=$1

file=(`ls $r`)

for f in ${file[@]}; do
    x=`echo $f | grep -E "$r" | grep -oE "$r[0-9]{2}"`
    x=`echo $x | grep -E "$r" | grep -oE "[0-9]{2}"`
    if [[ -n $x ]]; then
        mv $r/$f $r/$x.png
    fi
done