#include <stdio.h>
#include <omp.h>

int main()
{
	int ID = 0;	
	#pragma omp parallel
	printf("hello(%d)" , ID);
	printf("world(%d) \n", ID);
}