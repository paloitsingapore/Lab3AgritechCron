#!/bin/bash
date >> /home/pi/logs/poweroff.log
sleep 120
cd /home/pi/Lab3AgritechCron
filedate=$(stat -c %y update_status.txt | cut -d' ' -f1)
tdate=$(date +%F)
[[ -f update_status.txt ]] && finish_code=$(cat update_status.txt) || finish_code=1
if [ $filedate != $tdate ]; then
  ./RunUpdate.sh
elif [ $finish_code != 0 ]; then
  ./RunUpdate.sh
fi
