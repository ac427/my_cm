#!/bin/bash
input=$1
total_gpus=$(sinfo -o "%D %G" -t "idle,mixed,alloc,comp" | grep gpu | grep ":$input" | awk '{print $1}')
jobs_with_gpus_res=$(for i in $(squeue -h -o "%i" -t "running");do scontrol show job $i | grep "Gres=gpu" | awk -F'gpu:' '{print $2}' | awk '{print $1}';done | awk '{sum+=$1}END{print sum}')
gpu_jobs=$(for i in $(squeue -h -o "%i" -t "running");do scontrol show job $i | grep "Gres=gpu" > /dev/null; if [ $? -eq 0 ] ; then scontrol show job $i | grep "NodeList" | grep -v "ReqNode" | awk -F'=' '{print $2}'  ;fi; done | tr "\n" "\t") 
nodes_that_can_take_jobs=$(sinfo -o "%N %G" -t "idle,mixed" | grep gpu  | grep ":$input" | awk '{print $1}' ) 
#nodes_that_can_take_jobs=$(sinfo -o "%D %G" -t "idle,mixed" | grep gpu | awk '{print $1}')
echo "total gpus   $total_gpus "
echo "nodes that are having gpus jobs $gpu_jobs" 
echo "nodes that can accept new jobs $nodes_that_can_take_jobs" 
#echo "nodes that can accept new gpu jobs = nodes that can accept new jobs MINUS nodes that are having gpus jobs " 
#scontrol show hostname $(sinfo -o "%N %G" -t "idle,mixed" | grep gpu )
echo "nodes that can accept NEW gpu jobs"
for i in $(scontrol show hostname $nodes_that_can_take_jobs);
do 
scontrol show hostname $gpu_jobs | grep $i > /dev/null
if [ $? -ne 0 ];then
echo $i;
fi
done
