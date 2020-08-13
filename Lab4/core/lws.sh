#!/bin/bash
count=0
while :
do
    /usr/bin/python3 /home/pi/Lab3AgritechCron/Lab4/core/readLWS.py
    ((count++))
    echo "cycle" 
    echo $count
    sleep 10
done
