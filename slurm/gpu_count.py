#!/bin/env python
"""
program to check how many gpus are available

"""
 
import subprocess
import time
import re

NODE_GPU_VAL={}
NODE_CMD="scontrol  show nodes  "
NODE_CMD_OUT=subprocess.Popen(NODE_CMD,stdout=subprocess.PIPE,shell=True).communicate()[0].strip()
NODE_LIST_CMD=["sinfo -h -o '%N' | xargs scontrol show hostname > /tmp/.nodes"]
NODE_LIST_OUT=subprocess.Popen(NODE_LIST_CMD,stdout=subprocess.PIPE,shell=True).communicate()[0].strip()
file = open('/tmp/.nodes','r')
for node in file:
	NODE_GPU_VAL[node.rstrip('\n')]=0

NODE_LIST_GPU_CMD="for i in $(sinfo -o '%N %G' | grep gpu | awk '{print $1}');do scontrol show hostname $i;done > /tmp/.gpunodes"
NODE_LIST_OUT=subprocess.Popen(NODE_LIST_GPU_CMD,stdout=subprocess.PIPE,shell=True).communicate()[0].strip()
gpufile = open('/tmp/.gpunodes','r')
for gpunode in gpufile:
	GPU_COUNT_CMD="scontrol show node " + gpunode.rstrip('\n')  + " | grep 'Gres=gpu' | awk -F: '{print $2}'"
        NODE_GPU_VAL[gpunode.rstrip('\n')]=int(subprocess.Popen(GPU_COUNT_CMD,stdout=subprocess.PIPE,shell=True).communicate()[0].strip())
	#subprocess.Popen(GPU_COUNT_CMD,stdout=subprocess.PIPE,shell=True).communicate()[0].strip()

GPU_JOB_NODE_CMD="for i in $(squeue -h -o '%i' -t 'running');do scontrol show job $i  | egrep 'BatchHost|Gres=gpu' | tr ' ' '\n' | egrep 'Gres=gpu|BatchH' | tr '=' ':' | awk -F: 'BEGIN { ORS=\" \" }; {print $NF}' ; echo ' '  ;done  > /tmp/.gpurunning" 
GPU_JOB_NODE_OUT=subprocess.Popen(GPU_JOB_NODE_CMD,stdout=subprocess.PIPE,shell=True).communicate()[0].strip()

GPU_JOB_FILE= open(/tmp/.gpurunning)

