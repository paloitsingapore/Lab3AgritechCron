#!/bin/bash
#UPSTREAM=${1:-'@{u}'}
#LOCAL=$(git rev-parse @)
#REMOTE=$(git rev-parse "$UPSTREAM")
#BASE=$(git merge-base @ "$UPSTREAM")

#echo $LOCAL
#echo $REMOTE
#echo $BASE

 git pull
 for((i=1;i<11;i++))
 do
   if [ $? != 0 ]; then
     echo GIT pull failed , Waiting for 5 min for retry $i
     sleep 300     
     git pull   
   else
     break	   
   fi 	   
 done	 
 git diff --name-only HEAD HEAD~ >source_list.txt
 echo source list file update with source to be executed 
