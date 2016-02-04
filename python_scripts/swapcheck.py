#!/bin/env python
# Author Ananta Chakravartula
# script which check the stopped pids and reports 
import glob
import re
import os
lst = []
swap_tmp= ' '
swap_stopped=0
for file in glob.glob('/proc/*/status'):
    try:
    	pid_file = open(file).read()
	if re.search(r'stop',pid_file,flags=0):
		State = re.search(r'State:\s*\w*\s*\(stopped\)',pid_file)
    		if State: 
			print State.group()
		else:
			continue
		Name = re.search(r'Name:\s\w*',pid_file)
                if Name: print Name.group()
                Uid = re.search(r'Uid:\s\d+',pid_file)
                if Uid: print Uid.group()
		Pid = re.search(r'Pid:\s\d*',pid_file)
    		if Pid: print Pid.group()
		VmSwap = re.search(r'VmSwap:\s*\d*\s*\w*',pid_file)
    		if VmSwap: 
			print VmSwap.group(), "\n"
			swap_tmp=''.join(VmSwap.group())
			swap_kb=re.search(r'\d+',swap_tmp)
			lst.append(int(''.join(swap_kb.group())))
			
    except IOError:
	print "IO error", file
swap_Gb=sum(lst)/(1024*1024)
print 'Total Swap used by stopped process is ',sum(lst), 'kB', '=',swap_Gb,'Gb'
