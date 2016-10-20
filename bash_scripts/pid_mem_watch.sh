#!/bin/bash

#GLOBAL VARS
CPU=99
# MEMORY is % of system memory 
MEM=10
PS_FORMAT="uid,%cpu,%mem,bsdtime,user,pid,comm"
WHITELIST="sshd|sftp-server"
HOSTNAME=$(hostname -s)
# real work; 
while [ true ]
do
#sleep x minutes before checks
sleep 15m
tmp=$(date +%s) 
touch /tmp/$tmp
ps axo $PS_FORMAT |
awk '$1 > 1000 {print}' |
awk --assign C=$CPU --assign M=$MEM '$2 > C || $3 > M {print}' |
egrep -v "($WHITELIST)$" > /tmp/$tmp
checker=0

	for user in $(awk '{print $5}' /tmp/$tmp  | sort -u)
		do
		for pid in $(grep $user /tmp/$tmp | awk '{ print $6}')
			do
			if ps -p $pid > /dev/null
				then
				checker+=1
				fi
			done
	if [ $checker -ge 1 ]
		then
		
		# find user 
		# user_email=$(ldapsearch -LLL -x -H ldap://master.eth.cluster -b dc=cm,dc=cluster cn=$user | grep mail | awk '{print $2}') 
		# above is not working for all users; example dtalmy
		
		user_email=$(ldapsearch -LLL -x -H ldap://master.eth.cluster -b dc=cm,dc=cluster  "(objectclass=*)" 'mail' | grep -A 1 uid=$user, | grep mail | awk '{print $2}')
		# make call about the process; either send email or kill and send email 
#		echo "send email to " + $user_email +" to kill his processes "
		echo -e " uid,%cpu,%mem,bsdtime,user,pid,comm \n $(ps o  $PS_FORMAT  -u $user | awk '$1 > 1000 {print}' | awk --assign C=$CPU --assign M=$MEM '$2 > C || $3 > M {print}' | egrep -v "($WHITELIST)$" ) "  | mail -s "resource intensive process on $HOSTNAME" ac@techsquare.com
		
		else 
 		
		echo "pass" > /dev/null	
	fi	

		done
#clean up the file 
rm /tmp/$tmp
done
