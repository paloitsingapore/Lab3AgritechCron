#!/bin/bash
echo "There is nothing run"
echo "==========================================================="
echo "Doing Garbage Collection"
bash /home/pi/Lab3AgritechCron/GarbageCollection.sh
cd /home/pi/Lab3AgritechCron
myip=$(/sbin/ifconfig wlan0 | awk '/inet/  {gsub("addr:","",$2); print $2}' |awk 'NR==1{print $1}')

if [ "$myip" == 192.168.1.101 ] || [ "$myip" == 192.168.1.102 ];then
./addCron.sh "00 13-16 * * *"  "./home/pi/Lab3AgritechCron/ExtarctSystemRun.py" remove;
./addCron.sh "00 13-16 * * *"  "/usr/bin/python3 /home/pi/Lab3AgritechCron/ExtarctSystemRun.py" add;
fi

if [ "$myip" == 192.168.1.103 ];then
#./addCron.sh "1-59/2 * * * *"  "cd /home/pi/Lab3AgritechCron; /usr/bin/python3 schedular.py >> /home/pi/logs/schedular_systemlog.log" add;
./addCron.sh "* * * * *"  "cd /home/pi/Lab3AgritechCron; /usr/bin/python3 schedular.py >> /home/pi/logs/schedular_systemlog.log" add;
fi

if [ "$myip" == 192.168.1.104 ];then
#./addCron.sh "0-58/2 * * * *"  "cd /home/pi/Lab3AgritechCron; /usr/bin/python3 schedular.py >> /home/pi/logs/schedular_systemlog.log" add;
sed -i 's/localhost/192.168.1.102/g' /home/pi/Lab3AgritechCron/dbHandler.py
fi
