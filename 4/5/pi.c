#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <mpi.h>
#include <sys/time.h>

#define TRAP 1000
#define RUNS 200
#define MAX_ERR 1e-6

/* Function we are integrating */
double f(double x)
{
	return (4.0 / (1.0 + x*x));
}

double sec()
{
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return ((double) tv.tv_sec) +
		((double) tv.tv_usec) / 1e6;
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

void
comp(double *pi, int n)
{
	int my_rank, comm_sz, local_n;
	double local_a, local_b;
	int source;
	double local_int, total_int;
	double a, b, h;

	MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);

	//n = TRAP * comm_sz; /*number of trapezoids must be multiple of proc*/
	//n = 268435456;
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
		*pi = total_int;

	}
}

int main(int argc, char *argv[])
{
	int my_rank, i, p, n;
	double pi, t, times[RUNS];
	double mean = 0;
	double var = 0, std;

	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &p);

	if(argc != 2)
	{
		printf("Please, specify the input size n.\n");
		exit(1);
	}

	n = atoi(argv[1]);

	for(i=0; i<RUNS; i++)
	{
		MPI_Barrier(MPI_COMM_WORLD);

		t = sec();
		comp(&pi, n);


		if (my_rank == 0)
		{
			t = sec() - t;
			times[i] = t;
			mean += t;

			if(fabs(M_PI - pi) > MAX_ERR)
			{
				printf("The error is to big: %e\n", M_PI - pi);
				return 1;
			}
		}
	}
	if (my_rank == 0)
	{
		mean = mean/RUNS;


		for(i=0; i<RUNS; i++)
		{
			var += (mean - times[i]) * (mean - times[i]);
		}

		std = sqrt(var/(RUNS - 1));

		printf("%d,%d,%d,%f,%f\n", p, n, RUNS, 1000*mean, 1000*std);
	}

	MPI_Finalize();

	return 0;
}
