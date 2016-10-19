#!/bin/bash

#GLOBAL VARS
CPU=1
# MEMORY is % of system memory 
MEM=5
PS_FORMAT="uid,%cpu,%mem,bsdtime,user,pid,comm"
WHITELIST="sshd|sftp-server"
#create tmp file
tmp=$(date +%s) 
touch /tmp/$tmp

# real work; 
ps axo $PS_FORMAT |
awk '$1 > 1000 {print}' |
awk --assign C=$CPU --assign M=$MEM '$2 > C || $3 > M {print}' |
egrep -v "($WHITELIST)$" > /tmp/$tmp

while [ true ]
do

	for user in $(awk '{print $5}' /tmp/$tmp  | sort -u)
		do
		for pid in $(grep $user /tmp/$tmp | awk '{ print $6}')
			do
			if ps -p $pid > /dev/null
				then
				x+=1
				fi
			done
	if [ $x -ge 1 ]
		then
		
		# find user 
		# user_email=$(ldapsearch -LLL -x -H ldap://master.eth.cluster -b dc=cm,dc=cluster cn=$user | grep mail | awk '{print $2}') 
		# above is not working for all users; example dtalmy
		
		user_email=$(ldapsearch -LLL -x -H ldap://master.eth.cluster -b dc=cm,dc=cluster  "(objectclass=*)" 'mail' | grep -A 1 uid=$user, | grep mail | awk '{print $2}')
		
		# make call about the process; either send email or kill and send email 
		echo "send email to " + $user_email +" to kill his processes "
		
		else 
 		
		echo "pass" > /dev/null	
	fi	

		done
#clean up the file 
rm /tmp/$tmp
# sleep for x min
sleep 15m
done
