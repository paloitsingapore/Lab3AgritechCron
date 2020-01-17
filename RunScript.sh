#!/bin/bash
echo "There is nothing run"
echo "==========================================================="
echo "Doing Garbage Collection"
bash /home/pi/Lab3AgritechCron/GarbageCollection.sh
cd /home/pi/Lab3AgritechCron
myip=$(/sbin/ifconfig wlan0 | awk '/inet/  {gsub("addr:","",$2); print $2}' |awk 'NR==1{print $1}')
if [ "$myip" == 192.168.1.101 ] || [ "$myip" == 192.168.1.102 ];then 
./addCron.sh "00 13-16 * * *"  "./home/pi/Lab3AgritechCron/ExtarctSystemRun.py" add; 
fi

