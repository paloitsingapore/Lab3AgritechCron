#!/bin/bash
# Passing arguments to a function
get_docker_version()
{
	version=$(docker ps |grep "$1" |awk 'BEGIN { FS=":" } /1/ { print $2 }' | awk '{print $1}')
	echo $version
}

#Main Area 
get_docker_version
if [ -z "$version" ]
then
      newversion=1.0
else
      newversion=$(echo $version | awk '{ sum=$1+.1;print sum }')
fi

echo $newversion
out=$( { docker pull $1:$newversion; } 2>&1 )

#Docker Image Staus
if [[ $out == *"Image is up to date*" ]]
then
  echo image already updated
elif [[ $out == *"manifest unknown"* ]]
then
  echo  image not found
elif [[ $out == *"Downloaded newer image"* ]]
then
  echo pull done 
  git pull
  echo $?
fi	
