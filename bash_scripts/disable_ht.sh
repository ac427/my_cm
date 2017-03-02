#!/bin/bash 

# program works on both ubuntu and centos; ubuntu has cpus seperted with - and centos , 

CPU_OFFLINE=$( cat /sys/devices/system/cpu/cpu*/topology/thread_siblings_list | awk -F- '{print $2}' | sort -u) 
if [ -z "$CPU_OFFLINE" ] ; then
CPU_OFFLINE=$( cat /sys/devices/system/cpu/cpu*/topology/thread_siblings_list | awk -F, '{print $2}' | sort -u ) 
fi

for CPU in $CPU_OFFLINE
do
echo 0 > /sys/devices/system/cpu/cpu$CPU/online
done
