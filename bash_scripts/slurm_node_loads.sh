#!/bin/bash
# program to print load higher than total cpu 

TEMPFILE=$( mktemp --tmpdir=/tmp )
TEMPLOGFILE=$( mktemp --tmpdir=/tmp )
SPACE=','
#SPACE='\t '

scontrol show node | egrep "NodeName|CPULoad" |
#TO PRINT ALL CPU INFO 
#awk '{ if ($1 ~ /NodeName/) printf "\n %s,",$1; else if ($1 ~ /CPU/) for (i=1;i<=NF;i++)  printf "%s,",$i }' | tee $TEMPFILE

#IF YOU WANT JUST TOTAL CPU AND LOAD 
awk '{ if ($1 ~ /NodeName/) printf "\n %s,",$1; else if ($1 ~ /CPU/)  printf "%s,%s",$(NF-1),$NF}  END {printf "\n" }' | tee -a $TEMPFILE  > /dev/null

for lines in $(cat $TEMPFILE | grep -v "N/A");
do
	#CPUTot 
	CPUTot=$( echo $lines | awk -F, '{print $2}' | awk -F= '{print $2}')
	#CPULoad is load 
	CPULoad=$( echo $lines | awk -F, '{print $3}' | awk -F= '{print $2}')

	# rounding float to int 
	intCPULoad=${CPULoad%.*}
	# incrementing total cpu +1
	intCPUTot=$((CPUTot+1))

		if [ $intCPULoad -ge $intCPUTot ];	then
			echo $lines  | tee -a $TEMPLOGFILE
		fi
done

$(which mail) -s "Nodes with High CPULoad `hostname`" ac@techsquare.com < ${TEMPLOGFILE}

#echo  "Nodes with High CPULoad" | mail -s "Nodes with High CPULoad" -a $TEMPFILE ac@techsqaure.com 
rm $TEMPFILE
rm $TEMPLOGFILE
