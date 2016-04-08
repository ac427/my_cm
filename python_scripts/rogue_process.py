#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rouge_process.py
#  
#  Copyright 2016 Ananta Chakravartula <ac427@newton>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
"""
Script to find rogue process on compute nodes which bypassed LSF scheduler. LSF doesn't do proper cleanup for interactive jobs, example tmux will be lauched with ppid of 1 and when the job dies the process will be in sleeping state.
"""



import subprocess
import re

PIDS=[];
WHITELIST=['1']
LSFPIDS=[]
# get  all local account ; cut -d:  -f1 /etc/passwd
local_users_cmd=['cut', '-d:', '-f1', '/etc/passwd']
stdout=subprocess.Popen(local_users_cmd,stdout=subprocess.PIPE)
users=stdout.communicate()[0].replace('\n','|').rsplit('|',1)[0]
# get all pids excluding local accounts and 68 
process_cmd=["ps -ef | awk 'NR>1' | egrep -v \"68|"+users+" \"| awk '{print $2}' | sort -u" ]
process=directory_user_process=subprocess.Popen(process_cmd,stdout=subprocess.PIPE,shell=True).communicate()[0].strip()

## convert all pids to list 
for pid in process.split():
	PIDS.append(pid)

# get lsf process pids

LSF_PIDS=subprocess.Popen("service lsf status |   grep -o '[0-9]*'",stdout=subprocess.PIPE,shell=True).communicate()[0].strip()
for pid in LSF_PIDS.split():
	WHITELIST.append(pid)
	LSFPIDS.append(pid)

# get all the child and grand[grand*]-child process and put it in white list
for pid in LSFPIDS:
	for pid in subprocess.Popen('pstree -np '+pid+' | grep -o "[0-9]*"',stdout=subprocess.PIPE,shell=True).communicate()[0].strip().split():
		WHITELIST.append(pid)

# find rouge process
# print pid info ;  ps u -p 4220 | awk 'NR>1'
print "rogue pids " 
print "USER\tPID\tPPID\t%CPU\t%MEM\tSTAT\tTT\tTIME\t\tCMD"
for pid in PIDS:
	pid_info=['ps -p '+pid+'  -o user,pid,ppid,pcpu,pmem,stat,tty,time,cmd | awk "NR>1"']
	#pid_info=[' ps -f -p '+pid+ '| awk "NR>1"']
	if pid in WHITELIST:
		pass
	else:
		rogue_info=subprocess.Popen(pid_info,stdout=subprocess.PIPE,shell=True)
		print "\t".join(rogue_info.communicate()[0].split())
