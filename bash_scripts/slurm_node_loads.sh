#!/bin/bash
# program to print load higher than total cpu 

FILE=$( mktemp --tmpdir=/tmp )
SPACE=','
#SPACE='\t '

scontrol show node | egrep "NodeName|CPULoad" |
#TO PRINT ALL CPU INFO 
#awk '{ if ($1 ~ /NodeName/) printf "\n %s,",$1; else if ($1 ~ /CPU/) for (i=1;i<=NF;i++)  printf "%s,",$i }' | tee $FILE

#IF YOU WANT JUST TOTAL CPU AND LOAD 
awk '{ if ($1 ~ /NodeName/) printf "\n %s,",$1; else if ($1 ~ /CPU/)  printf "%s,%s",$(NF-1),$NF}  END {printf "\n" }' | tee $FILE  > /dev/null

for lines in $(cat $FILE | grep -v "N/A");
do
	#x is total cpu 
	x=$( echo $lines | awk -F, '{print $2}' | awk -F= '{print $2}')
	#y is load 
	y=$( echo $lines | awk -F, '{print $3}' | awk -F= '{print $2}')

	# rounding float to int 
	inty=${y%.*}
	# incrementing total cpu +1
	intx=$((x+1))

		if [ $inty -ge $intx ];	then
			echo $lines 
		fi
done
rm $FILE
