#!/bin/bash
#Passing arguments to a function like agritechpaloit/webapp ,agrtechpaloit/cratedb
repo=$1
get_latest_version()
{
  newversion=$(./GetLatestImage.sh $repo)
  echo $newversion
}

pull_docker()
{	
        get_latest_version
	out=$( { sudo docker pull $newversion; } 2>&1 )
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
	  imagename=$newversion
	  imagefile=$(echo "$imagename" | sed "s/\//_/g")
	  sudo docker save $imagename $newversion | gzip > /home/pi/bin/DockerImages/$imagefile.tar.gz
	fi	
}

#Main Area 
echo pulling docker
pull_docker

