#!/bin/bash
mkdir -p /home/$USER/log 
LOG="/home/$USER/log/top_users.$(date +%F).log"
date +%m%d%y_%H_%M >> $LOG
top icb -n 1 | grep -A 10 USER >> $LOG

