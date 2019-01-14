#!/bin/bash

GPUS="1 2 4 8 16 32"
for p in $GPUS; do
	NODES="$(((p+3)/4))"
	TASKS_PER_NODE="$(($p<4 ? $p : 4))"
	sed \
		-e "s/_NODES_/$NODES/g" \
		-e "s/_GPUS_/$GPUS/g" \
		-e "s/_TASKS_PER_NODE_/$TASKS_PER_NODE/g" \
		job-base > job.$p

	sbatch job.$p
done
