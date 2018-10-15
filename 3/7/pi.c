#include <math.h>
#include <stdlib.h>
#include <stdio.h>

/* Function we are integrating */
double f(double x){
	return (4.0 / (1.0 + x*x));
}

/* Calculate local integral */
double TrapezoidalRule( double a, double b, double h, int n)
{
	double EstimatedArea, x;
	int i;

	EstimatedArea = (f(a) + f(b))/2.0;
	for (i = 1; i <= n-1; i++) {
		x = a+ i*h;
		EstimatedArea += f(x);
	}
	EstimatedArea = EstimatedArea*h;
	return EstimatedArea;
}

int main(int argc, char *argv[])
{
	int n;
	printf("Enter the number of subintervals: ");
	scanf("%d",&n);

	double a=0;
	double b=1;
	double h = (b-a) / (double) n;

	double pi = TrapezoidalRule(a, b, h, n);
	printf("With n = %d trapezoids, ", n);
	printf("the integral from %f to %f is %.15e\n", a, b, pi);
}
