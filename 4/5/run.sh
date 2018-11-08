#!/bin/bash

#THREADS="32 16 8 4 2"
THREADS="1 2 4 8 16 32"
SIZES="65536 1048576 16777216 268435456"

echo -e "p,n,runs,mean time ms,std time ms"

for N in $SIZES; do
	for T in $THREADS; do
		mpirun -n $T ./pi $N
	done
done
