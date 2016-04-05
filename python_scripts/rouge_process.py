#!/bin/env python
import subprocess
import re

PIDS=[];

#cut -d:  -f1 /etc/passwd
local_users_cmd=['cut', '-d:', '-f1', '/etc/passwd']
stdout=subprocess.Popen(local_users_cmd,stdout=subprocess.PIPE)
users=stdout.communicate()[0].replace('\n','|').rsplit('|',1)[0]
process_cmd=["ps -ef | awk 'NR>1' | egrep -v \""+users+" \"| awk '{print $3}'" ]
directory_user_process=subprocess.Popen(process_cmd,stdout=subprocess.PIPE,shell=True)
#directory_user_process.stdin.write("egrep -v \"" + users+"\"")
process=directory_user_process.communicate()[0].strip()
for i in process.split():
	try:
		PIDS.append(re.search(r'\d+',i).group())
	except AttributeError:
		pass 
#print users.replace('\n','|').rsplit('|',1)[0]
# find ppid of 2426; ps -p 2426 -o ppid=
print PIDS
