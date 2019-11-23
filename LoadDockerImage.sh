#/bin/bash
cd /home/pi/bin/DockerImages
for f in *.tar.gz; 
do 
 echo "Loading  $f file to Docker Image "; 
 zcat $f | sudo docker load
 if [ $? -eq 0 ]; then
   sudo rm $f	 
 fi 	 
 echo "Loaded to Docker Images"
done
