#!/bin/bash
sho=agritechpaloit/webapp:1.2
sho1=$(echo "$sho" | awk '/1/ -F "/^" {print $1}')
echo $sho1
t=$(echo "$sho" | sed "s/\//_/g")
echo $t
docker save $sho | gzip > /home/pi/$t.tar.gz
