#!/usr/bin/env bash

file=(`ls`)

for f in ${file[@]}; do
    x=`echo $f | grep -E "^Map"`
    if [[ -n $x ]]; then
        ffile=(`ls $f`)
        for ff in ${ffile[@]}; do
            y=`echo $ff | grep -E "\.png$"`
            if [[ -n $y ]]; then
                z=`echo $ff | grep -E "map[0-9]{2}"`
                mv $f/$ff map/
            else
                mv $f/$ff info/
            fi
        done
    fi
done