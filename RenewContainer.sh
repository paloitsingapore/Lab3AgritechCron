#!/bin/bash
#set -ex
cont_repo=$1

#Function

GetLatestImage()
{
  
  echo $1	
  images=$(docker images | grep $cont_repo  |awk {'print $2'})
  echo Available Tags $images
}

#Main
GetLatestImage
# loop through all containers
OldImage=.9
for image in $images
do

 if (( $(echo "$image $OldImage" | awk '{print ($1 > $2)}') )); then
   OldImage=$image	
 fi
done
RContID=$(docker ps | grep $cont_repo | awk '{print $1}')
RimageName=$(docker ps | grep agritechpaloit/webapp | awk '{print $2}')
AimageName=$cont_repo:$OldImage

echo Currently Running $RimageName
echo Latest Available Image $AimageName
if [ "$RimageName" != "$AimageName" ]; then
   docker stop $RContID
   echo Container Stopped $RContID
   docker rm $RContID
   echo Container Removed $RContID
   if [[ $cont_repo == *"webapp"* ]]; then
     echo Running New Docker Image $AimageName	   
     docker run -d -p 3000:3000 $AimageName
     echo waiting for 1 min to check container is alive 
     sleep 1m
     CcontName=docker ps | grep $AimageName | awk {'print $2'}  
     if [ -z "$CcontName"]; then
      AContID=$(docker ps -a | grep $AimageName | awk '{print $1}')
      docker rm $AContID      
      echo New Conatiner is not alive $AimageName
      echo Restarting old Conatiner $RimageName
      docker run -d -p 3000:3000 $RimageName
      echo $RimageName started             
     fi 
   elif [[ $cont_repo == *"cratedb"* ]]; then 
     docker run  -d --net crate -p 4200:4200 --name node1 -p 4300:4300 -e CRATE_HEAP_SIZE=64m -v /etc/sysctl.conf:/etc/sysctl.conf -v /home/pi/crate-4.0.7/da     ta:/home/crate/crate/data -v /home/pi/crate-4.0.7/config/:/home/crate/crate/config/  agritechpaloit/cratedb:1.0 /bin/bash -c "bin/crate -Cnetwork.host=_site_,_local_"   
   fi

else
    echo "Strings are  equal"
fi

