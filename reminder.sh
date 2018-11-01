#!/bin/bash


for terminal  in $(who |grep tbricks | awk '{print $2}')
do 
    echo -e "This is your reminder...\n\n" > /dev/$terminal
done
