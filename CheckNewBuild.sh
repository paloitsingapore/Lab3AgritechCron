#!/bin/bash
# Checking GIT PULL Requird
set -ex
repo=$1
UpdateScript()
{
UPSTREAM=${1:-'@{u}'}
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse "$UPSTREAM")
BASE=$(git merge-base @ "$UPSTREAM")

if [ $LOCAL = $REMOTE ]; then
    echo "Up-to-date"
elif [ $LOCAL = $BASE ]; then
   git pull 
   git diff --name-only HEAD HEAD~ >source_list.txt
   echo source list file update with source to be executed 
fi


}
#Passing arguments to a function
get_docker_version()
{
	echo $repo
	version=$(docker ps |grep "$repo" |awk 'BEGIN { FS=":" } /1/ { print $2 }' | awk '{print $1}')
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
  echo Downloding Updated Script form GITHUB
  UpdateScript
fi	
