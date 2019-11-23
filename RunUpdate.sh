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
 LogFileRunScipt=RunScript.sh.$Date.log

 #Running Script
   echo getting GIT UPDATE....
  ./GitUpdate.sh > /home/pi/logs/$LogFileNameGitUpd
  echo Running CheckNewBuild.sh for webapp.....
  ./CheckNewBuild.sh webapp >/home/pi/logs/$LogFileNameWebApp
  echo Running CheckNewBuild.sh for cratedb....
  ./CheckNewBuild.sh cratedb >/home/pi/logs/$LogFileNameCrateDB 
  echo coping Data to other pi ....
 
 
 echo Renewing Container ....
 #master pi
	if [ "$myip" == 192.168.1.101 ];then
                 ./CopyUpdate.sh 192.168.1.102 192.168.1.103  >> /home/pi/logs/$LogFileNameCopyUpd
		 ./RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 #1st Pi
		 ./ssh -l pi 192.168.1.102 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./ssh -l pi 192.168.1.102 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> /home/pi/logs/LogFileNameRenewCont
		
		 #2nd Pi
		 ./ssh -l pi 192.168.1.103 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./ssh -l pi 192.168.1.103 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> /home/pi/logs/LogFileNameRenewCont
		
		 #3rd Pi
		 #./ssh -l pi 192.168.1.104 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 #./ssh -l pi 192.168.1.104 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> /home/pi/logs/LogFileNameRenewCont
		 
		 echo Running Script ....
		 ./RunScript.sh > /home/pi/logs/$LogFileRunScipt
		  #Run Script to other 2 pi
        	   ssh -l pi 192.168.1.102 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
		   ssh -l pi 192.168.1.103 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
	   	   #ssh -l pi 192.168.1.104 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
        
	   elif [ "$myip" == 192.168.1.102 ];then
                 ./CopyUpdate.sh 192.168.1.101 192.168.1.103  > /home/pi/logs/$LogFileNameCopyUpd

		 ./RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 #1st Pi
		 ./ssh -l pi 192.168.1.101 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./ssh -l pi 192.168.1.101 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> LogFileNameRenewCont
		
		 #2nd Pi
		 ./ssh -l pi 192.168.1.103 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./ssh -l pi 192.168.1.103 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> /home/pi/logs/LogFileNameRenewCont
		
		 #3rd Pi
		 #./ssh -l pi 192.168.1.104 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 #./ssh -l pi 192.168.1.104 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> /home/pi/logs/LogFileNameRenewCont
		 
		 echo Running Script ....
		 ./RunScript.sh > /home/pi/logs/$LogFileRunScipt

		  #Run Script to other 2 pi
		   ssh -l pi 192.168.1.101 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
		   ssh -l pi 192.168.1.103 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
	   	   #ssh -l pi 192.168.1.104 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt

          elif [ "$myip" == 192.168.1.103 ];then
	         ./CopyUpdate.sh 192.168.1.101 192.168.1.102 > /home/pi/logs/$LogFileNameCopyUpd
	
		 ./RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 #1st Pi
		 ./ssh -l pi 192.168.1.101 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./ssh -l pi 192.168.1.101 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> LogFileNameRenewCont
		
		 #2nd Pi
		 ./ssh -l pi 192.168.1.102 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./ssh -l pi 192.168.1.102 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> /home/pi/logs/LogFileNameRenewCont
		
		 #3rd Pi
		 #./ssh -l pi 192.168.1.104 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 #./ssh -l pi 192.168.1.104 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> /home/pi/logs/LogFileNameRenewCont
		 
		 echo Running Script ....
		 ./RunScript.sh > /home/pi/logs/$LogFileRunScipt
		 #Run Script to other 2 pi
		 ssh -l pi 192.168.1.101 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
	   	 ssh -l pi 192.168.1.102 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
	   	 #ssh -l pi 192.168.1.104 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt

          elif [ "$myip" == 192.168.1.104 ];then
	         ./CopyUpdate.sh 192.168.1.101 192.168.1.102 192.168.1.103 > /home/pi/logs/$LogFileNameCopyUpd
	
		 ./RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 #1st Pi
		 ./ssh -l pi 192.168.1.101 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./ssh -l pi 192.168.1.101 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> LogFileNameRenewCont
		
		 #2nd Pi
		 ./ssh -l pi 192.168.1.102 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./ssh -l pi 192.168.1.102 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> /home/pi/logs/LogFileNameRenewCont
		
		 #3rd Pi
		 ./ssh -l pi 192.168.1.103 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/webapp >> /home/pi/logs/LogFileNameRenewCont
		 ./ssh -l pi 192.168.1.103 /home/pi/Lab3AgritechCron/RenewContainer.sh lab3agritechpaloit/cratedb >> /home/pi/logs/LogFileNameRenewCont
		 
		 echo Running Script ....
		 ./RunScript.sh > /home/pi/logs/$LogFileRunScipt
		 #Run Script to other 2 pi
		 ssh -l pi 192.168.1.101 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
	   	 ssh -l pi 192.168.1.102 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
	   	 ssh -l pi 192.168.1.103 /home/pi/Lab3AgritechCron/RunScript.sh >> /home/pi/logs/LogFileRunScipt
         fi

else
 echo Not The Master Node
fi

