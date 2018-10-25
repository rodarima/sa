#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include <sys/time.h>

#define RUNS 5
#define MAX_ERR 1e-6

struct timeval start_time, end_time;

void print_times() 
{
	int total_usec;
	float total_time, total_flops;
	total_usec = (end_time.tv_sec - start_time.tv_sec) * 1000000 +
		(end_time.tv_usec - start_time.tv_usec);
	printf(" %.2f mSec \n", ((float) total_usec) / 1000.0);
	total_time = ((float) total_usec) / 1000000.0;
}

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
	int i, thread_count, res;

	if(!argv[1])
	{
		printf("Please, specify the number of threads\n");
		return 1;
	}

	thread_count = strtol(argv[1], NULL, 10);

	for(i = 0; i<RUNS; i++)
	{
		gettimeofday(&start_time, NULL);
		res = comp(thread_count);
		gettimeofday(&end_time, NULL);
		if (res)
		{
			printf("Computation failed\n");
			return 1;
		}
		print_times();
	}

	return 0;
}
