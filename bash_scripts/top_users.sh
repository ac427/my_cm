#!/bin/bash
. /home/ac427/.bashrc

LOG="/home/ac427/log/top_users.$(date +%F).$(hostname).log"
echo $LOG
date >> $LOG
/usr/bin/top -cbn 1 | head -20 | grep -A 10 COMMAND >> $LOG
