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
RimageID=$(docker ps | grep $cont_repo | awk '{print $1}')
docker stop $RimageID


