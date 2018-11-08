## Task 4.1
*Populate the Table 4.1 and analyze the results for the program that
estimates the number π.*

We slightly modified the table to include the mean and std of 200 runs,
measuring the running time of the program.

	Table 4.1

	|p       |runs    |mean time ms    |std time ms|
	|:------:|:------:|:--------------:|:---------:|
	|2       |200     |136.260248      |0.540395   |
	|4       |200     |68.743345       |1.807676   |
	|8       |200     |34.402916       |2.805065   |
	|16      |200     |17.196037       |0.919341   |
	|32      |200     |8.641697        |0.534061   |

And the program:

	% cat pi.c
	#include <stdio.h>
	#include <stdlib.h>
	#include <math.h>
	#include <omp.h>
	#include <sys/time.h>

	#define RUNS 5
	#define MAX_ERR 1e-6

	struct timeval start_time, end_time;

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

## Task 4.2
*Populate the Table 4.2 and analyze the results for the program that estimates
the number π. Compare the results from Table 4.1 and Table 4.2.*

	Table 4.2

	|p       |runs    |mean time ms    |std time ms|
	|:------:|:------:|:--------------:|:---------:|
	|2       |200     |136.010271      |1.422983   |
	|4       |200     |67.964889       |0.698149   |
	|8       |200     |34.164717       |1.013572   |
	|16      |200     |16.987933       |0.360736   |
	|32      |200     |8.511111        |0.267816   |

We see that as the number of processes **p** doubles, the average running time
almost goes half.

	% cat pi.c
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
	comp(double *pi)
	{
		int my_rank, comm_sz, n, local_n;
		double local_a, local_b;
		int source;
		double local_int, total_int;
		double a, b, h;

		MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
		MPI_Comm_size(MPI_COMM_WORLD, &comm_sz);

		//n = TRAP * comm_sz; /*number of trapezoids must be multiple of proc*/
		n = 268435456;
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
		int my_rank, i, p;
		double pi, t, times[RUNS];
		double mean = 0;
		double var = 0, std;

		MPI_Init(&argc, &argv);
		MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
		MPI_Comm_size(MPI_COMM_WORLD, &p);

		for(i=0; i<RUNS; i++)
		{
			MPI_Barrier(MPI_COMM_WORLD);

			t = sec();
			comp(&pi);


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

			printf("%d\t%d\t%f\t%f\n", p, RUNS, 1000*mean, 1000*std);
		}

		MPI_Finalize();

		return 0;
	}


