#!/bin/bash

a=2
b=3
c=$( awk -v min=$a -v max=$b 'BEGIN{srand(); print min+rand()*(max-min)}' )
echo $c
#echo $(date +%s)
#sleep $c
#echo $(date +%s)
