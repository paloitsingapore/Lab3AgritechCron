#!/bin/bash
echo "This Script will node delete node module"
set -o errexit

echo "Removing exited docker containers..."
docker ps -a -f status=exited -q | xargs -r docker rm -v

echo "Removing untagged images..."
docker images --no-trunc | grep "<none>" | awk '{print $3}' | xargs -r docker rmi

echo "Removing unused docker images"
images=($(docker images | tail -n +2 | awk '{print $1":"$2}'))
containers=($(docker ps -a | tail -n +2 | awk '{print $2}'))

containers_reg=" ${containers[*]} "
remove=()

for item in ${images[@]}; do
  if [[ ! $containers_reg =~ " $item " ]]; then
    if [[ $item != *"node"*  ]]; then    
    	remove+=($item)
    fi
  fi
done

remove_images=" ${remove[*]} "

echo ${remove_images} | xargs -r docker rmi
echo "Done"
