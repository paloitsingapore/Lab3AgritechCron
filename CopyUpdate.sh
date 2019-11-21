#!/bin/bash
for var in "$@"
do
   echo  Replicating GitUpdate and Docker Image tp $var ....
   #Send Script to other nodes
    cat source_list.txt | while read line || [[ -n $line ]];
    do
     # do something with $line here
     if [[ ! -z $line ]]; then
      scp  /home/pi/Lab3AgritechCron/$line  pi@$var:/home/pi/Lab3AgritechCron
     fi
    done
    scp -r /home/pi/Lab3AgritechCron/.git pi@$var:/home/pi/Lab3AgritechCron/

    #Send Docker Image to other Nodes
    scp -r  /home/pi/bin/DockerImages pi@$var:/home/pi/bin/
    if [ $? -eq 0 ]; then
       ssh -l pi $var /home/pi/Lab3AgritechCron/LoadDockerImage.sh
    else
      echo Image transfer not completed
    fi	
    echo "" > source_list.txt
    echo  Replication Completed ...    
done

