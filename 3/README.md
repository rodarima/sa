## Getting started with parallel programming models

### Task 3.1

Check the loaded modules in your environment.

	% module list
	Currently Loaded Modules:
	  1) intel/2017.4   2) impi/2017.4   3) mkl/2017.4   4) bsc/1.0

### Task 3.2

Create, compile and run a Hello World program with MPI.

	% cat mpi_helloworld.c
	#include <mpi.h>
	#include <stdio.h>

	int main (int argc, char **argv)
	{
		int size, rank;
		MPI_Init (&argc, &argv);
		MPI_Comm_rank(MPI_COMM_WORLD, &rank);
		MPI_Comm_size (MPI_COMM_WORLD, &size);
		printf ( "I am %d of %d\n", rank, size );
		MPI_Finalize();

		return 0;
	}

	% mpicc mpi_helloworld.c -o mpi_helloworld

	% mpirun ./mpi_helloworld
	I am 0 of 48
	I am 4 of 48
	I am 15 of 48
	I am 27 of 48
	I am 28 of 48
	I am 37 of 48
	I am 38 of 48
	I am 40 of 48
	I am 41 of 48
	I am 42 of 48
	I am 46 of 48
	I am 1 of 48
	I am 2 of 48
	...
	I am 36 of 48
	I am 20 of 48
	I am 24 of 48

### Task 3.3

Submit your "Hello World" program.

The job script:

	% cat job
	#!/bin/bash
	#SBATCH --job-name="MPI_HelloWorld"
	#SBATCH --workdir=.
	#SBATCH --output=output_%J.out
	#SBATCH --error=output_%J.err
	#SBATCH --ntasks=16
	#SBATCH --tasks-per-node=8
	#SBATCH --time=00:01:00
	#SBATCH --exclusive
	#SBATCH --qos=debug

	mpirun ./mpi_helloworld

When it's submitted:

	% sbatch job

	% squeue
		     JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
		   2500123      main MPI_Hell sam14015 PD       0:00      2 (Priority)
	% squeue
		     JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
		   2500123      main MPI_Hell sam14015  R       0:05      2 s05r2b[64,66]
	% squeue
		     JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
		   2500123      main MPI_Hell sam14015 CG       0:10      2 s05r2b[64,66]
	% squeue
		     JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
		   2500123      main MPI_Hell sam14015 CG       0:10      1 s05r2b66
	% squeue
		     JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)

Check the output of the execution. What happened with the order of outputs?

	% cat output*.out
	I am 1 of 16
	I am 2 of 16
	I am 5 of 16
	I am 6 of 16
	I am 7 of 16
	I am 0 of 16
	I am 3 of 16
	I am 4 of 16
	I am 10 of 16
	I am 9 of 16
	I am 8 of 16
	I am 15 of 16
	I am 12 of 16
	I am 11 of 16
	I am 14 of 16
	I am 13 of 16

It's not sorted.

### Task 3.4

Modify your solution that just prints a line of output from each process so that
the output is printed in process rank order: process 0 output first, then
process 1, and so on.

	% cat mpi_helloworld.c
	#include <mpi.h>
	#include <stdio.h>

	int main (int argc, char **argv)
	{
		int size, rank, dummy=0;
		MPI_Init (&argc, &argv);
		MPI_Comm_rank(MPI_COMM_WORLD, &rank);
		MPI_Comm_size (MPI_COMM_WORLD, &size);

		if (rank != 0)
		{
			MPI_Recv(&dummy, 1, MPI_INT, rank-1,
				0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		}

		printf("I am %d of %d\n", rank, size);

		if (rank < size-1)
		{
			MPI_Send(&dummy, 1, MPI_INT, rank+1,
				0, MPI_COMM_WORLD);
		}

		MPI_Finalize();

		return 0;
	}

	% mpicc mpi_helloworld.c -o mpi_helloworld

	% mpirun ./mpi_helloworld
	I am 0 of 48
	I am 1 of 48
	I am 2 of 48
	I am 3 of 48
	I am 4 of 48
	...
	I am 42 of 48
	I am 43 of 48
	I am 44 of 48
	I am 45 of 48
	I am 46 of 48
	I am 47 of 48

Now is sorted.

### Task 3.5

When compiling and running the sequential code the output is the following:

	% ./hello
	hello(0)world(0)

The most basic OpenMP parallelization is adding the `omp parallel` directive: 

	#include <stdio.h>
	#include <omp.h>

	int main(){
			int ID = 0;
			#pragma omp parallel
			printf("hello(%d)", ID);
			printf("world(%d) \n", ID);
			return 0;
	}

If we execute the program now we can observe the following output:
	
	% ./hello
	hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
	hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
	hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
	hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
	hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)\
	hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)hello(0)world(0)

We notice that "hello" was printed 48 times, which means that 48 threads are created.
In the case that we don't specify the number of threads in the `omp parallel` directive
the runtime system determines how many of them to spawn.

### Task 3.6

We can change the code in order to print the rank of each thread as it executes.
For this we use `omp_get_thread_num()` and `omp_get_num_threads()` functions:

	#include <stdio.h>
	#include <omp.h>

	void hello(void);

	int main(){
			#pragma omp parallel
			hello();
			return 0;
	}

	void hello(void){
			int my_rank = omp_get_thread_num();
			int thread_count = omp_get_num_threads();

			printf("Hello from thread %d of %d\n", my_rank, thread_count);
	}

As we would expect, the output prints `x out of 48` for each thread:

	% ./hello
	Hello from thread 0 of 48
	Hello from thread 16 of 48
	Hello from thread 7 of 48
	Hello from thread 4 of 48
	Hello from thread 30 of 48
	Hello from thread 34 of 48
	Hello from thread 17 of 48
	Hello from thread 43 of 48
	Hello from thread 41 of 48
	Hello from thread 45 of 48
	Hello from thread 31 of 48
	Hello from thread 19 of 48
	Hello from thread 3 of 48
	Hello from thread 47 of 48
	Hello from thread 6 of 48
	Hello from thread 27 of 48
	Hello from thread 46 of 48
	Hello from thread 9 of 48
	Hello from thread 24 of 48
	Hello from thread 25 of 48
	Hello from thread 44 of 48
	Hello from thread 12 of 48
	Hello from thread 2 of 48
	Hello from thread 5 of 48
	Hello from thread 23 of 48
	Hello from thread 20 of 48
	Hello from thread 28 of 48
	Hello from thread 22 of 48
	Hello from thread 21 of 48
	Hello from thread 11 of 48
	Hello from thread 10 of 48
	Hello from thread 15 of 48
	Hello from thread 13 of 48
	Hello from thread 14 of 48
	Hello from thread 1 of 48
	Hello from thread 18 of 48
	Hello from thread 32 of 48
	Hello from thread 35 of 48
	Hello from thread 37 of 48
	Hello from thread 39 of 48
	Hello from thread 29 of 48
	Hello from thread 42 of 48
	Hello from thread 8 of 48
	Hello from thread 40 of 48
	Hello from thread 33 of 48
	Hello from thread 26 of 48
	Hello from thread 36 of 48
	Hello from thread 38 of 48

We notice that threads don't execute in order of their rank. 
In fact, the order depends on how the scheduler assigns execution of each thread.

In order to make the threads execute in order of rank, use the `omp ordered` directive:
	
	#include <stdio.h>
	#include <omp.h>

	void hello(void);

	int main(){
			#pragma omp parallel
			hello();
			return 0;
	}

	void hello(void){
			int my_rank = omp_get_thread_num();
			int thread_count = omp_get_num_threads();
			#pragma omp ordered
			printf("Hello from thread %d of %d\n", my_rank, thread_count);
	}

At this point, each thread executes in order of its rank:

	% ./hello
	Hello from thread 0 of 48
	Hello from thread 1 of 48
	Hello from thread 2 of 48
	Hello from thread 3 of 48
	Hello from thread 4 of 48
	Hello from thread 5 of 48
	Hello from thread 6 of 48
	Hello from thread 7 of 48
	Hello from thread 8 of 48
	Hello from thread 9 of 48
	Hello from thread 10 of 48
	Hello from thread 11 of 48
	Hello from thread 12 of 48
	Hello from thread 13 of 48
	Hello from thread 14 of 48
	Hello from thread 15 of 48
	Hello from thread 16 of 48
	Hello from thread 17 of 48
	Hello from thread 18 of 48
	Hello from thread 19 of 48
	Hello from thread 20 of 48
	Hello from thread 21 of 48
	Hello from thread 22 of 48
	Hello from thread 23 of 48
	Hello from thread 24 of 48
	Hello from thread 25 of 48
	Hello from thread 26 of 48
	Hello from thread 27 of 48
	Hello from thread 28 of 48
	Hello from thread 29 of 48
	Hello from thread 30 of 48
	Hello from thread 31 of 48
	Hello from thread 32 of 48
	Hello from thread 33 of 48
	Hello from thread 34 of 48
	Hello from thread 35 of 48
	Hello from thread 36 of 48
	Hello from thread 37 of 48
	Hello from thread 38 of 48
	Hello from thread 39 of 48
	Hello from thread 40 of 48
	Hello from thread 41 of 48
	Hello from thread 42 of 48
	Hello from thread 43 of 48
	Hello from thread 44 of 48
	Hello from thread 45 of 48
	Hello from thread 46 of 48
	Hello from thread 47 of 48

### Task 3.7

### Task 3.8

Create and execute a MPI program that estimates the number PI.

	% cat pi.c
	#include <math.h>
	#include <stdlib.h>
	#include <stdio.h>
	#include <mpi.h>

	#define TRAP 1000

	/* Function we are integrating */
	double f(double x)
	{
		return (4.0 / (1.0 + x*x));
	}

	/* Calculate local integral */
	double TrapezoidalRule( double a, double b, double h, int n)
	{
		double EstimatedArea, x;
		int i;
		EstimatedArea = (f(a) + f(b))/2.0;
		for (i = 1; i <= n-1; i++)
		{
			x = a+ i*h;
			EstimatedArea += f(x);
		}
		EstimatedArea = EstimatedArea*h;
		return EstimatedArea;
	}

	int main(int argc, char *argv[])
	{
		int my_rank, comm_sz, n, local_n;
		double local_a, local_b;
		int source;
		double local_int, total_int;
		double a, b, h;

		MPI_Init(&argc, &argv);
		MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
		MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);

		n = TRAP * comm_sz; /*number of trapezoids must be multiple of proc*/
		a = 0;
		b = 1;

		h = (b-a) / (double)n;
		local_n = n/comm_sz;
		local_a = a + my_rank*local_n*h;
		local_b = local_a + local_n*h;
		local_int = TrapezoidalRule(local_a, local_b, h, local_n);

		if (my_rank != 0)
		{
			MPI_Send(&local_int, 1, MPI_DOUBLE, 0, 0, MPI_COMM_WORLD);
		}
		else
		{
			total_int = local_int;
			for (source = 1; source < comm_sz; source++)
			{
				MPI_Recv(&local_int, 1, MPI_DOUBLE, source, 0,
					MPI_COMM_WORLD, MPI_STATUS_IGNORE);
				total_int += local_int;
			}
		}

		if (my_rank == 0)
		{
			printf("With n = %d trapezoids, ", n);
			printf("from %f to %f is %.15e\n", a, b, total_int);
		}

		MPI_Finalize();

		return 0;
	}

	% make
	mpicc     pi.c  -lm -o pi

	% mpirun ./pi
	With n = 48000 trapezoids, from 0.000000 to 1.000000 is 3.141592653517455e+00

### Task 3.9

Task 3.9: Create and execute a OpenMP program `pi_openmp.c` to estimate the
value of number Π. Consider the number of theads is a parameter. The input data
a, b, n are hardwired for simplicity.


