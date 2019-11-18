#!/bin/bash
Date=$(date +"%F%T")
echo $Date
LogFileNameWebApp=agritechpaloit_webapp.$Date.log
LogFileNameCrateDB=agritechpaloit_cratedb.$Date.log
echo $LogFileNameWebApp
echo $LogFileNameCrateDB
./CheckNewBuild.sh agritechpaloit/webapp >/home/pi/logs/$LogFileNameWebApp
./CheckNewBuild.sh agritechpaloit/cratedb >/home/pi/logs/$LogFileNameCrateDB

