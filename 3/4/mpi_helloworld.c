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
