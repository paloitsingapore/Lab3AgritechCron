#!/bin/bash
#testPassing arguments to a function like agritechpaloit/webapp ,agrtechpaloit/cratedb
repo=$1
get_latest_version()
{
  newversion=$(./GetLatestImage.sh $repo)
  echo $newversion
}

pull_docker()
{	
       #Docker Image Staus  
        get_latest_version
	out=$(docker pull $newversion 2>docker_pull.txt  | tee; ( exit ${PIPESTATUS[0]})) 
        pull_exit_code=$?
        err=$(cat docker_pull.txt)	
	a=5
	b=6
	for (( i=1; i<17; i++ )) 
	do   
   		   	if [ $a -gt 60 ]; then
	     			a=60
		   	fi   

			if [ $pull_exit_code != 0 ]                        
			then                                
				echo Docker Pull Failed......
				echo Error $err
				echo -n "Retry $i Wating for $a - min for retry....." 
			        sleeptime=$((a * 60))	
				sleep $sleeptime
 				get_latest_version
				out=$(docker pull $newversion 2>docker_pull.txt  | tee; ( exit ${PIPESTATUS[0]}))				
				pull_exit_code=$? 
                                echo =================================================================
				err=$(cat docker_pull.txt)
				echo $err
                                echo =================================================================				
			   	fn=$((a + b)) 
			   	a=$b 
			   	b=$fn 

			else 
                          break 	
			fi  
         done
	echo $out 
	if [[ $out == *"Image is up to date"* ]]
	then
	  echo Image already updated
	elif [[ $out == *"manifest unknown"* ]]
	then
	  echo  image not found
	elif [[ $out == *"Downloaded newer image"* ]]
	then
	  echo New image downloded ,Zipping the image
	  imagename=$newversion
	  imagefile=$(echo "$imagename" | sed "s/\//_/g")
	  sudo docker save $imagename $newversion | gzip > /home/pi/bin/DockerImages/$imagefile.tar.gz
	fi	
}

#Main Area 
echo pulling docker
pidfile=$0.pid
if [ ! -f ${pidfile} ] ||  ! ps -p `cat ${pidfile}` >/dev/null; then
 echo $$ >${pidfile}
 pull_docker
else
 echo "Process is already running"
 exit -1
fi
