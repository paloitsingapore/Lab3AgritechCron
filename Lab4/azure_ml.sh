/usr/bin/python3 /home/pi/Lab3AgritechCron/Lab4/extractSoilData.py
/usr/bin/python3 /home/pi/Lab3AgritechCron/Lab4/extractSettings.py
sleep 10
docker cp b78260ee38e0:/home/crate/crate/data/azdata/ /home/pi/data/
sleep 10
/usr/bin/python3 /home/pi/Lab3AgritechCron/Lab4/loadSoilData.py
sleep 10
/usr/bin/python3 /home/pi/Lab3AgritechCron/Lab4/loadSettings.py
sleep 10