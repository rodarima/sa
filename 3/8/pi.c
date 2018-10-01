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
