#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include <sys/time.h>

#define RUNS 200
#define MAX_ERR 1e-6

double sec()
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return ((double) tv.tv_sec) +
		((double) tv.tv_usec) / 1e6;
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
	//n=1e4; /*16^7 */
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
	int i, p, res;
	double t, times[RUNS], mean=0, var=0, std;

	if(!argv[1])
	{
		printf("Please, specify the number of threads\n");
		return 1;
	}

	p = strtol(argv[1], NULL, 10);

	for(i = 0; i<RUNS; i++)
	{
		t = sec();
		res = comp(p);
		t = sec() - t;
		if (res)
		{
			printf("Computation failed\n");
			return 1;
		}
		times[i] = t;
		mean += t;
		//fprintf(stderr, "i=%d t=%f\n", i, t);
	}

	mean = mean/RUNS;

	for(i=0; i<RUNS; i++)
	{
		var += (mean - times[i]) * (mean - times[i]);
	}

	std = sqrt(var/(RUNS - 1));

	printf("%d\t%d\t%f\t%f\n", p, RUNS, 1000*mean, 1000*std);

	return 0;
}
