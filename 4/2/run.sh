#!/bin/bash

#THREADS="32 16 8 4 2"
THREADS="2 4 8 16 32"

rm -f results.txt

for T in $THREADS; do
	mpirun -n $T ./pi | tee -a results.txt
done
