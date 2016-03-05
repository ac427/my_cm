#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  NFSMountcheck.py
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
import subprocess
import time


def fscheck():
	space=" "
        mountpoint_cmd = '/bin/mountpoint'
        mountpoint_args = '-q'
        filesystems = { 'var': '/var', 'log': '/log', 'apps':'/share/apps'}
        result ={}
        for fs in filesystems:
                cmd=[mountpoint_cmd,mountpoint_args,filesystems[fs]]
                mount_check = subprocess.Popen(cmd)
## Introducing delay as mount_check is not that quick in getting result, if it take more than 5ms then probably slow NFS, we can adjust time as required
                time.sleep(0.005)
                if mount_check.poll() == 0:
                        result[fs]="1"
                
		if mount_check.poll() == None:
                
		        try:
                                mount_check.kill()
                        except:
                                pass
                        result[fs]="0"
                
		if mount_check.poll() == 1:
                        result[fs]="0"
        
	returnvalue=str(len(filesystems))+space
	for key in result:
			returnvalue+= key+space+result[key]+space
			
	print returnvalue

def main():
	
	while True:
		fscheck()
		time.sleep(60)

if __name__ == '__main__':
        main()
