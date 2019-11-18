#!/bin/bash
set -ex
cont_repo=$1

#Function

GetLatestImage()
{
  
  echo $1	
  images=$(docker images | grep $cont_repo  |awk {'print $2'})
  echo $images
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

echo $RimageName
echo $AimageName
if [ "$RimageName" != "$AimageName" ]; then
   docker stop $RContID
   echo Container Stopped $RContID
   docker rm $RContID
   echo Container Removed $RContID
   echo "$cont_repo"
   if [[ $cont_repo == *"webapp"* ]]; then
     echo Running New Docker Image $AimageName	   
     docker run -d -p 3000:3000 $AimageName
   elif [[ $cont_repo == *"cratedb"* ]]; then 
     docker run  -d --net crate -p 4200:4200 --name node1 -p 4300:4300 -e CRATE_HEAP_SIZE=64m -v /etc/sysctl.conf:/etc/sysctl.conf -v /home/pi/crate-4.0.7/da     ta:/home/crate/crate/data -v /home/pi/crate-4.0.7/config/:/home/crate/crate/config/  agritechpaloit/cratedb:1.0 /bin/bash -c "bin/crate -Cnetwork.host=_site_,_local_"   
   fi

else
    echo "Strings are  equal"
fi

