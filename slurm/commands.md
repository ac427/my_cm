### srun

```
## run two tasks on two nodes 
[21:35 ac@eofe4 ~]$srun -p sched_mit_hill -N2 -n2  -exclusive hostname
srun: job 5689688 queued and waiting for resources
srun: job 5689688 has been allocated resources
node338
node394

## run 4 tasks on two nodes 
[21:36 ac@eofe4 ~]$srun -p sched_mit_hill -N2 -n4  -exclusive hostname
srun: job 5689745 queued and waiting for resources
srun: job 5689745 has been allocated resources
node338
node394
node394
node394
# run 2 tasks/per node on 2 nodes 
[21:38 ac@eofe4 ~]$srun -p sched_mit_hill -N2 --ntasks-per-node=2  -exclusive hostname
srun: job 5689785 queued and waiting for resources
srun: job 5689785 has been allocated resources
node387
node387
node388
node388


```
