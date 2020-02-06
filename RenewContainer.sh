#!/bin/bash
#set -ex
cont_repo=$1

#Function

GetLatestImage()
{
  
  echo $1	
  images=$(sudo docker images | grep $cont_repo  |awk {'print $2'})
  echo Available Tags $images
}

#Main
echo =======================================================
GetLatestImage
# loop through all containers
OldImage=.9
for image in $images
do

 if (( $(echo "$image $OldImage" | awk '{print ($1 > $2)}') )); then
   OldImage=$image	
 fi
done
RContID=$(sudo docker ps | grep $cont_repo | awk '{print $1}')
RimageName=$(sudo docker ps | grep $cont_repo | awk '{print $2}')
AimageName=$cont_repo:$OldImage

echo Currently Running $RimageName
echo Latest Available Image $AimageName
if [ "$RimageName" != "$AimageName" ]; then

   if [[ ! -z "$RimageName" ]]; then	
   	sudo docker stop $RContID
   	echo Container Stopped $RContID
   	sudo docker rm $RContID
   	echo Container Removed $RContID
   fi
   if [[ $cont_repo == *"webapp"* ]]; then
     echo Running New Docker Image $AimageName	   
     sudo docker run -d -p 3000:3000 -e TZ=Asia/Singapore $AimageName
     echo waiting for 1 min to check container is alive 
     sleep 1m     
     CcontName=$(sudo docker ps | grep $AimageName | awk {'print $2'}) 
     if [ -z "$CcontName" ];then
      AContID=$(sudo docker ps -a | grep $AimageName | awk '{print $1}')
      sudo docker rm $AContID    
      echo New Conatiner is not alive $AimageName
      echo Restarting old Conatiner $RimageName
      sudo docker run -d -p 3000:3000 -e TZ=Asia/Singapore --restart on-failure $RimageName
      echo $RimageName started   
     else
      #--restart on-failure     
      Ccontid=$(sudo docker ps | grep $AimageName | awk {'print $1'})
      docker update --restart on-failure $Ccontid
      echo Restart Policy Added 
     fi 
   elif [[ $cont_repo == *"cratedb"* ]]; then 
     echo Running New Docker Image $AimageName
     sudo sudo docker run  -d --net crate -p 4200:4200  -p 4300:4300 -e CRATE_HEAP_SIZE=512m -v /etc/sysctl.conf:/etc/sysctl.conf -v /home/pi/crate-4.0.6/data:/home/crate/crate/data -v /home/pi/crate-4.0.6/config/:/home/crate/crate/config/  $AimageName /bin/bash -c "bin/crate -Cnetwork.host=_site_,_local_"   
     echo waiting for 1 min to docker container is alive 
     sleep 1m
     CcontName=$(sudo docker ps | grep $AimageName | awk {'print $2'})  
     if [ -z "$CcontName" ]; then
      AContID=$(sudo docker ps -a | grep $AimageName | awk '{print $1}')
      sudo docker rm $AContID      
      echo New Conatiner is not alive $AimageName
      echo Restarting old Conatiner $RimageName
      sudo docker run  -d --net crate -p 4200:4200  -p 4300:4300 --restart on-failure  -e CRATE_HEAP_SIZE=512m -v /etc/sysctl.conf:/etc/sysctl.conf -v /home/pi/crate-4.0.6/data:/home/crate/crate/data -v /home/pi/crate-4.0.6/config/:/home/crate/crate/config/  $RimageName /bin/bash -c "bin/crate -Cnetwork.host=_site_,_local_"   
      echo $RimageName startedLab3AgritechCron
     else
      #--restart on-failure     
      Ccontid=$(sudo docker ps | grep $AimageName | awk {'print $1'})    
      docker update --restart on-failure $Ccontid 
      echo Restart Policy added
     fi
   fi

else
    echo "Container with latest images is running"
fi


