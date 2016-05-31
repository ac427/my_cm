#!/bin/bash

total_gpus=$(sinfo -o "%D %G" -t "idle,mixed,alloc,comp" | grep gpu | awk '{print $1}')
jobs_with_gpus_res=$(for i in $(squeue -h -o "%i" -t "running");do scontrol show job $i | grep "Gres=gpu" | awk -F'gpu:' '{print $2}' | awk '{print $1}';done | awk '{sum+=$1}END{print sum}')
if [ -z $jobs_with_gpus_res ]; then
jobs_with_gpus_res=0
fi
total_gpus_avail=$(echo "$total_gpus - $jobs_with_gpus_res"| bc)
echo $total_gpus_avail
