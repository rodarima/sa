Task 3.9: Create and execute a OpenMP program pi.c to estimate the value
of number PI. Consider the number of theads is a parameter. The input data a,
b, n are hardwired for simplicity. Use the following code as a base and include
the parallel pragma for parallelizing and use a critical directive for global
sum (each thread explicitly computes the integral over its assigned
subinterval).

	#include <stdio.h>
	#include <stdlib.h>
	#include <math.h>
	#include <omp.h>

	double f(double x)
	{
		return (4.0 / (1.0 + x*x));
	}

	double TrapezoidalRule(double a, double b, int n)
	{
		double h, x, my_result;
		double local_a, local_b;

		int i, local_n;
		int my_rank = omp_get_thread_num();
		int thread_count = omp_get_num_threads();
		h = (b-a)/n;
		local_n = n/thread_count;
		local_a = a + my_rank*local_n*h;
		local_b = local_a + local_n*h;
		my_result = (f(local_a) + f(local_b))/2.0;


		for (i = 1; i <= local_n-1; i++)
		{
			x = local_a + i*h;
			my_result += f(x);
		}
		return my_result*h;
	}

	int main(int argc, char* argv[])
	{
		double global_result = 0.0;
		double a, b;
		int n;
		int thread_count;

		if(!argv[1])
		{
			printf("Please, specify the number of threads\n");
			return 1;
		}

		n=268435456; /*16^7 */
		a=0;
		b=1;
		thread_count = strtol(argv[1], NULL, 10);

		global_result = 0.0;
	#pragma omp parallel num_threads(thread_count) reduction(+:global_result)
		global_result += TrapezoidalRule(a, b, n);
		printf("OpenMP with %d threads and  n = %d trapezoids, ",
				thread_count,n);
		printf("the integral from %f to %f is  %.15e\n", a, b,
				global_result);
		return 0;
	}

To measure the time, more reliably, the computation is repeated 100 times, and
the time is measured of the whole execution.


	#include <stdio.h>
	#include <stdlib.h>
	#include <math.h>
	#include <omp.h>

	#define RUNS 100
	#define MAX_ERR 1e-6

	double f(double x)
	{
		return (4.0 / (1.0 + x*x));
	}

	double TrapezoidalRule(double a, double b, int n)
	{
		double h, x, my_result;
		double local_a, local_b;

		int i, local_n;
		int my_rank = omp_get_thread_num();
		int thread_count = omp_get_num_threads();
		h = (b-a)/n;
		local_n = n/thread_count;
		local_a = a + my_rank*local_n*h;
		local_b = local_a + local_n*h;
		my_result = (f(local_a) + f(local_b))/2.0;


		for (i = 1; i <= local_n-1; i++)
		{
			x = local_a + i*h;
			my_result += f(x);
		}
		return my_result*h;
	}

	int comp(int thread_count)
	{
		double global_result = 0.0;
		double a, b;
		int n;

		n=268435456; /*16^7 */
		a=0;
		b=1;

		global_result = 0.0;
	#pragma omp parallel num_threads(thread_count) reduction(+:global_result)
		global_result += TrapezoidalRule(a, b, n);
		//printf("OpenMP with %d threads and  n = %d trapezoids, ",
		//		thread_count,n);
		//printf("the integral from %f to %f is  %.15e\n", a, b,
		//		global_result);
		
		if(fabs(M_PI - global_result) > MAX_ERR)
		{
			printf("The error is to big: %e\n", M_PI - global_result);
			return 1;
		}

		return 0;
	}

	int main(int argc, char* argv[])
	{
		int i, thread_count;

		if(!argv[1])
		{
			printf("Please, specify the number of threads\n");
			return 1;
		}

		thread_count = strtol(argv[1], NULL, 10);

		for(i = 0; i<RUNS; i++)
		{
			if (comp(thread_count))
			{
				printf("Computation failed\n");
				return 1;
			}
		}

		return 0;
	}

As the number of threads grow, the execution time is reduced, until we pass the
number of threads of the machine (48):

	% ./run.sh   
	Running with 1 thread(s)

	real    0m27.233s
	user    0m27.218s
	sys     0m0.008s
	Running with 2 thread(s)

	real    0m13.661s
	user    0m27.281s
	sys     0m0.020s
	Running with 4 thread(s)

	real    0m6.858s
	user    0m27.344s
	sys     0m0.012s
	Running with 8 thread(s)

	real    0m3.435s
	user    0m27.375s
	sys     0m0.000s
	Running with 16 thread(s)

	real    0m1.728s
	user    0m27.394s
	sys     0m0.012s
	Running with 32 thread(s)

	real    0m0.896s
	user    0m27.783s
	sys     0m0.020s
	Running with 64 thread(s)

	real    0m1.672s
	user    0m33.722s
	sys     0m40.234s
