#!/bin/bash
#
# Broadband usage monitoring script
#    Copyright (C) 2013 Steven Kay
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
# 
# This is a Unix shell script I wrote to allow me to monitor my (not-unlimited) broadband usage, and also to
# get a feel for the bandwidth requirements of certain applications, downloads and sites.
#
# This is intended to be run from a cron job on a minute-by-minute basis (or at least, several times an hour)
# For example, 
# */1 * * * * /home/steven/dumpusage.sh
#
# This script writes to a csv log, scraping the output of ifconfig
# The file format is
#
# Timestamp (yyyymmddhhmm), Bytes Downloaded, Bytes Uploaded
#
# The number of bytes is a snapshot of the total, NOT the number of bytes since the last execution 
# If the system is rebooted or you log out, these totals are reset
#
# If running from cron, you'll need to make sure that ifconfig is added to the path in cron, and that the log file is
# writable by whatever user cron is running under
# 
# Use the report.py python script provided to provide a nicer view of the data
#

interface="eth1"

if [ ! -f ~/bandwidth.csv ]
then
    echo -e "Timestamp,Bytes Downloaded,Bytes Uploaded" >> ~/bandwidth.csv
fi
echo -n `date "+%Y%m%d%H%M"` >> ~/bandwidth.csv
echo -n -e "," >> ~/bandwidth.csv
echo -n -e `ifconfig -a $interface | grep "RX bytes" | sed "s/TX.*//" | sed "s/.*[:]//" | sed "s/\s.*//"` >> ~/bandwidth.csv
echo -n -e "," >> ~/bandwidth.csv
echo `ifconfig -a $interface | grep "TX bytes" | sed "s/.*TX bytes[:]//" | sed "s/[(].*[)]//"` >> ~/bandwidth.csv
