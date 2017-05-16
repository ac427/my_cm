#!/bin/bash
# program to print load higher than total cpu 

TEMPFILE=$( mktemp --tmpdir=/tmp )
TEMPLOGFILE=$( mktemp --tmpdir=/tmp )
SPACE=','
#SPACE='\t '

scontrol show -o node | egrep "NodeName|CPULoad"  | awk 'BEGIN {OFS=","} {print $1,$6,$7}' | tee $TEMPFILE > /dev/null

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
