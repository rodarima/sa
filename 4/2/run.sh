#!/bin/bash

#THREADS="32 16 8 4 2"
THREADS="2 4 8 16 32"

echo -e "p\truns\tmean time ms\tstd time ms"

for T in $THREADS; do
	mpirun -n $T ./pi
done
