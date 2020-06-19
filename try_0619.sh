#!/bin/bash

a=2
b=5
c=$( awk -v min=$a -v max=$b 'BEGIN{ "date +%N" | getline seed; srand(seed); print min+rand()*(max-min)}' )
echo $c
#echo $(date +%s)
#sleep $c
#echo $(date +%s)
