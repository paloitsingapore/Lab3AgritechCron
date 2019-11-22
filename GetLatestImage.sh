#!/bin/bash


# set username and password
UNAME="lab3agritechpaloit"
UPASS="paloit"
key="$1"

# get token to be able to talk to Docker Hub
TOKEN=$(curl -s -H "Content-Type: application/json" -X POST -d '{"username": "'${UNAME}'", "password": "'${UPASS}'"}' https://hub.docker.com/v2/users/login/ | jq -r .token)

# get list of namespaces accessible by user (not in use right now)
#NAMESPACES=$(curl -s -H "Authorization: JWT ${TOKEN}" https://hub.docker.com/v2/repositories/namespaces/ | jq -r '.namespaces|.[]')

# get list of repos for that user account

  IMAGE_TAGS=$(curl -s -H "Authorization: JWT ${TOKEN}" https://hub.docker.com/v2/repositories/${UNAME}/${key}/tags/?page_size=10000 | jq  '.results|.[]|.name,.last_updated')

  #echo ================================================================================================
  #echo ${IMAGE_TAGS}
  #echo ================================================================================================
  # build a list of images from tags
  k=0
  l=0
  timestamp=""
  ver=""
  flag=0

   for j in ${IMAGE_TAGS}
   do
     if [[ $((k % 2)) -eq 1 ]]; then 
	 [[ -z "$timestamp" ]] && timestamp=$j || [[ "$timestamp" < "$j" ]] && timestamp=$j
     fi
     k=$k+1
  done

  for i in ${IMAGE_TAGS}
  do
      if [[ $((l % 2)) -eq 0 ]]; then
	      ver=$i
      else
	      [[ "$i" == "$timestamp" ]] && ver=${ver%\"} && ver=${ver#\"} && echo ${UNAME}/${key}:${ver} && exit 
      fi

      l=$l+1
  done	  

