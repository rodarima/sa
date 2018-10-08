#include <math.h>
3 #include <stdlib.h>
4 #include <stdio.h>
56
/* Function we are integrating */
7 double f(double x){
8 return (4.0 / (1.0 + x*x));
9 }
10
11 /* Calculate local integral */
12 double TrapezoidalRule( double a, double b, double h, int n)
13 {
14 double EstimatedArea, x;
15 int i;
16
17 EstimatedArea = (f(a) + f(b))/2.0;
18 for (i = 1; i <= n-1; i++) {
19 x = a+ i*h;
20 EstimatedArea += f(x);
21 }
22 EstimatedArea = EstimatedArea*h;
23 return EstimatedArea;
24 }
25
26 int main(int argc, char *argv[])
27 {
28 int n;
29 printf("Enter the number of subintervals: ");
30 scanf("%d",&n);
31
32 double a=0;
33 double b=1;
34 double h = (b-a) / (double) n;
35
36 double pi = TrapezoidalRule(a, b, h, n);
37 printf("With n = %d trapezoids, ", n);
38 printf("the integral from %f to %f is %.15e\n", a, b, pi);
39 }