#!/bin/bash

GPUS="1 2 4 8 16 32"
for p in $GPUS; do
	NODES="$(((p+3)/4))"
	TASKS_PER_NODE="$(($p<4 ? $p : 4))"
	sed -e "s/NODES/$NODES/g" \
		-e "s/TASKS_PER_NODE/$TASKS_PER_NODE/g" \
		job-base > job.$p

	sbatch job.$p
done
