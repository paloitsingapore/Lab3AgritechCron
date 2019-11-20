#!/bin/bash
#Passing arguments to a function
repo=$1
get_docker_version()
{
	echo $repo
	version=$(docker ps |grep "$repo" |awk 'BEGIN { FS=":" } /1/ { print $2 }' | awk '{print $1}')
	echo $version
}

pull_docker()
{

	get_docker_version
	if [ -z "$version" ]
	then
	      newversion=1.0
	else
	      newversion=$(echo $version | awk '{ sum=$repo+.1;print sum }')
	fi
	
	echo $repo:$newversion
	out=$( { docker pull $repo:$newversion; } 2>&1 )
	echo $out
	#Docker Image Staus
	if [[ $out == *"Image is up to date"* ]]
	then
	  echo Image already updated
	elif [[ $out == *"manifest unknown"* ]]
	then
	  echo  image not found
	elif [[ $out == *"Downloaded newer image"* ]]
	then
	  echo New image downloded
	  imagename=$repo:$newversion
	  imagefile=$(echo "$imagename" | sed "s/\//_/g")
	  docker save $imagename | gzip > /home/pi/bin/DockerImages/$imagefile.tar.gz
	fi	
}

#Main Area 
echo pulling docker
pull_docker

