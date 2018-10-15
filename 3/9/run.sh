#!/bin/bash

THREADS="1 2 4 8 16 32 64"

for T in $THREADS; do
	echo "Running with $T thread(s)"
	time ./pi $T
done
