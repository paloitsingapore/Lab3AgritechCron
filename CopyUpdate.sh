#!/bin/bash
for var in "$@"
do
   echo  Replicating GitUpdate and Docker Image tp $var ....
   #Send Script to other nodes
    ssh -l pi $var chmod -R 777 /home/pi/Lab3AgritechCron/.git
    scp -r /home/pi/Lab3AgritechCron pi@$var:/home/pi/ 
    #Send Docker Image to other Nodes
    scp  /home/pi/bin/DockerImages/* pi@$var:/home/pi/bin/DockerImages/
    if [ $? -eq 0 ]; then
       ssh -l pi $var /home/pi/Lab3AgritechCron/LoadDockerImage.sh
    else
      echo Image transfer not completed
    fi	
    echo  Replication Completed ...    
done
chmod -R 777 /home/pi/Lab3AgritechCron/.git
echo Deleting Docker image fIles 
sudo rm -r  /home/pi/bin/DockerImages/*
echo "" > source_list.txt
echo File Deleted....
