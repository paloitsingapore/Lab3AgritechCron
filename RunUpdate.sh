#!/bin/bash
myip=$(ifconfig wlan0 | awk '/inet/  {gsub("addr:","",$2); print $2}' |awk 'NR==1{print $1}')
masterip=$(/usr/bin/python3 IsMaster.py)
echo My IP $myip
echo Master IP $masterip
if [ "$masterip" == "$ip" ];then
 Date=$(date +"%F%T")
 #LogFileName ...
 LogFileNameWebApp=agritechpaloit_webapp_CheckNewBuild.$Date.log
 LogFileNameCrateDB=agritechpaloit_cratedb_CheckNewBuild.$Date.log
 LogFileNameGitUpd=GitUpdateGitUpdate.sh$Date.log
 LogFileNameCopyUpd=CopyUpdate.sh.$Date.log
 LogFileNameRenewCont=RenewConatiner.sh.$Date.log
 LogFileRunScipt= RunScript.sh.$Date.log

 #Running Script
 ./CheckNewBuild.sh webapp >/home/pi/logs/$LogFileNameWebApp
 ./CheckNewBuild.sh cratedb >/home/pi/logs/$LogFileNameCrateDB
 ./GitUpdate.sh > /home/pi/logs/$LogFileNameGitUpd
 ./CopyUpdate.sh 172.16.14.108 > /home/pi/logs/$LogFileNameCopyUpd

  #1st Pi
 ./ssh -l pi 172.16.14.108 /home/pi/Lab3AgritechCron/RenewConatiner.sh agritechpaloit/webapp >> LogFileNameRenewCont
 ./ssh -l pi 172.16.14.108 /home/pi/Lab3AgritechCron/RenewConatiner.sh agritechpaloit/cratedb >> LogFileNameRenewCont

  #2nd Pi
  #./ssh -l pi 172.16.14.108 /home/pi/Lab3AgritechCron/RenewConatiner.sh agritechpaloit/webapp >> LogFileNameRenewCont
  #./ssh -l pi 172.16.14.108 /home/pi/Lab3AgritechCron/RenewConatiner.sh agritechpaloit/cratedb >> LogFileNameRenewCont

  #3rd Pi
  #./ssh -l pi 172.16.14.108 /home/pi/Lab3AgritechCron/RenewConatiner.sh agritechpaloit/webapp >> LogFileNameRenewCont
  #./ssh -l pi 172.16.14.108 /home/pi/Lab3AgritechCron/RenewConatiner.sh agritechpaloit/cratedb >> LogFileNameRenewCont

 ./RunScript.sh > /home/pi/logs/$LogFileRunScipt
  #Run Script to other 2 pi
  #ssh -l pi 172.16.14.108 /home/pi/Lab3AgritechCron/RunScript.sh agritechpaloit/cratedb >> LogFileRunScipt
  #ssh -l pi 172.16.14.108 /home/pi/Lab3AgritechCron/RunScript.sh agritechpaloit/cratedb >> LogFileRunScipt

else
 echo Not The Master Node
fi

