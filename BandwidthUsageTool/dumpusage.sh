#!/bin/bash
# writes the total number of bytes received and transmitted over a network interface
# used as a poor man's bandwidth monitoring utility for those, like me, without all-you-can-eat broadband plans :)
# writes to ~/bandwidth.log
# if running from cron, remember to make sure that the cron path is set up to find ifconfig, and that the bandwidth.log
# has permissions set to allow writing from the cron job user

interface="eth1"

if [ ! -f ~/bandwidth.csv ]
then
    echo -e "Timestamp,Bytes Downloaded,Bytes Uploaded" >> ~/bandwidth.csv
fi
echo -n `date` >> ~/bandwidth.csv
echo -n -e "," >> ~/bandwidth.csv
echo -n -e `ifconfig -a $interface | grep "RX bytes" | sed "s/TX.*//" | sed "s/.*[:]//" | sed "s/\s.*//"` >> ~/bandwidth.csv
echo -n -e "," >> ~/bandwidth.csv
echo `ifconfig -a $interface | grep "TX bytes" | sed "s/.*TX bytes[:]//" | sed "s/[(].*[)]//"` >> ~/bandwidth.csv
