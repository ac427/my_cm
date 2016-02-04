#!/bin/bash
LOG="top_users.$(date +%F).log"
echo $LOG
date >> $LOG
top icb -n 1 | grep -A 10 USER >> $LOG

