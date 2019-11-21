#!/bin/bash
#!/bin/bash
for var in "$@"
do
    cat source_list.txt | while read line || [[ -n $line ]];
    do
     # do something with $line here
     if [[ ! -z $line ]]; then
      scp  /home/pi/Lab3AgritechCron/$line  pi@$var:/home/pi/Lab3AgritechCron
     fi
    done
done

