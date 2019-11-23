#/bin/bash
cd /home/pi/bin/DockerImages/
for f in *.tar.gz; 
do 
 echo "Loading  $f file to Docker Image "; 
 zcat $f | sudo docker load
 if [ $? -eq 0 ]; then
   sudo rm $f
   echo "Loaded to Docker Images"
 echo 
  echo "Docker Image Load Failed"	 
 fi 	 
 
done
