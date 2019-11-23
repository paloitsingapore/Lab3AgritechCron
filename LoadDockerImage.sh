#/bin/bash
cd /home/pi/bin/DockerImages/
myip=$(ifconfig wlan0 | awk '/inet/  {gsub("addr:","",$2); print $2}' |awk 'NR==1{print $1}')
for f in *.tar.gz; 
do 
 echo "Loading  $f file to Docker Image "; 
 if [ "$myip" == 192.168.1.104 ];then
	 
	 if [[ $f != *"crate"* ]];then
	 	zcat $f | sudo docker load
 	 fi

 else 
     zcat $f | sudo docker load
 fi
 if [ $? -eq 0 ]; then
   sudo rm $f
   echo "Loaded to Docker Images"
 else
  echo "Docker Image Load Failed"	 
 fi 	 
 
done
