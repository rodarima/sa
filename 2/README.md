## Lab 2 - Getting started with supercomputing

### 2.3 Marenostrum file systems
Active Archive has 2 dedicated machines (dt01.bsc.es and dt02.bsc.es) for access
while GPFS can be accessed from any machine.

Active Archive has special commands for managing that actually submit a job:
dtcp, dtmv, dtrsync, dttar

Jobs can be viewed and canceled with: dtq, dtcancel

These commands also accept special flags: blocking (block read access) and time
(max transfer time)

These jobs can be submitted from both login machines and dt machines.

On the other hand GPFS can be managed through the standard commands: cp, mv,
sync, tar

Also Active Archive doesn't perform any data backup, while GPFS performs a
daily, incremental backup for /gpfs/home and /gpfs/projects.

### 2.4 ?

### 2.5 Available queues

	QUEUE NAME     MAX TIME   MAX PROC
	       debug     02:00:00        768
	 interactive     02:00:00          4
	    training   2-00:00:00        768

### 2.6 Job script

	#!/bin/bash
	#SBATCH --job-name="hello world"
	#SBATCH --workdir=.
	#SBATCH --output=output_%J.out
	#SBATCH --error=output_%J.err
	#SBATCH --ntasks=1
	#SBATCH --tasks-per-node=1
	#SBATCH --time=00:01:00
	#SBATCH --exclusive
	#SBATCH --qos=debug
	./hi; sleep 30 > serial.out
