#!/bin/bash

THREADS="2 4 8 16"

for T in $THREADS; do
	echo "Running with $T thread(s)"
	./pi $T
done
