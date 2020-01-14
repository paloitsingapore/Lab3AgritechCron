#!/bin/bash        
# usage: addCron '<interval>' '<command>' <add|remove>
# ./addCron.sh "*/15 * * * *" "./home/pi/Lab3AgritechCron/LoadDataS3.py" add
# ./addCron.sh "*/15 * * * *" "./home/pi/Lab3AgritechCron/LoadDataS3.py" "remove"
# To Update the Schedule just change the Schedule and keep common at same with add
# To Update Cron 1st Remove it the add 




if [[ -z "$1" ]] ;then printf " no interval specified\n" ;fi
if [[ -z "$2" ]] ;then printf " no command specified\n" ;fi
if [[ -z "$3" ]] ;then printf " no action specified\n" ;fi

if [[ "$3" == add ]] ;then
    # add cronjob, no duplication:
    ( crontab -l | grep -v -F -w "$2" ; echo "$1 $2" ) | crontab -
elif [[ "$3" == remove ]] ;then
    # remove cronjob:
    ( crontab -l | grep -v -F -w "$2" ) | crontab -
fi 
