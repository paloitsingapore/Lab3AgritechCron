#!/bin/bash
#UPSTREAM=${1:-'@{u}'}
#LOCAL=$(git rev-parse @)
#REMOTE=$(git rev-parse "$UPSTREAM")
#BASE=$(git merge-base @ "$UPSTREAM")

#echo $LOCAL
#echo $REMOTE
#echo $BASE

 git pull 
 git diff --name-only HEAD HEAD~ >source_list.txt
 echo source list file update with source to be executed 
