#!/bin/bash
myip=$(ifconfig wlan0 | awk '/inet/  {gsub("addr:","",$2); print $2}' |awk 'NR==1{print $1}')
masterip=$(/usr/bin/python3 IsMaster.py)
echo My IP $myip
echo Master IP $masterip
if [ "$masterip" == "$ip" ];then
 Date=$(date +"%F%T")
 LogFileNameWebApp=agritechpaloit_webapp_CheckNewBuild.$Date.log
 LogFileNameCrateDB=agritechpaloit_cratedb_CheckNewBuild.$Date.log
 #Running Script
 ./CheckNewBuild.sh agritechpaloit/webapp >/home/pi/logs/$LogFileNameWebApp
 ./CheckNewBuild.sh agritechpaloit/cratedb >/home/pi/logs/$LogFileNameCrateDB
 ./LookForGitUpdate.sh
 ./CopyUpdate.sh
 ./RunScript.sh
else
 echo Not The Master Node
fi

