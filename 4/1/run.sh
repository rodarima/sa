#!/bin/bash

THREADS="2 4 8 16"

echo -e "p\truns\tmean time ms\tstd time ms"

for T in $THREADS; do
	./pi $T
done
