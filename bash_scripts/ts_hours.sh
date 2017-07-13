#!/bin/bash
rm tmp.txt
awk -F',' 'BEGIN{OFS="|";} {print $1,$2,$3,$5,$6,$7,$8,$9;}' $1 | tr "," "|" >> tmp.txt 

start_date=$2
#start_date=2016-09-02
#num_days=30
num_days=$3
for i in `seq 0 $num_days`; do date=`date +%Y-%m-%d -d "${start_date}+${i} days"` ; grep $date tmp.txt  > $date-ac; done
