## Lab 5: Getting started with parallel performance models

<div style="text-align: right">authors: Arias Rodrigo, Burca Horia</div>

<div style="text-align: right">date: 12/11/2018</div>

## Task 5.1

*Analize with your partner both codes 5.1 and 5.2 that implement a matrix-
vector multiplication. Write in the report of this laboratory the main
differences of both codes.*

The main difference is that the sequential program does all the operations
sequentially, while the parallel code distributes the work among different
processes, and then computes the work in parallel.

The parallelization of the matrix vector product is done by scattering across
the processors the rows of the matrix A in groups, scattering the vector and then
all-gathering it in the processors, multiplying the local parts of A by the
vector in order to get a part of the resulting vector and then gathering all the
parts in order to get the full result.

Also, the initialization of the matrices is always performed in sequential.

## Task 5.2

*Analize Table 5.3 and explain what happened with the relation of terms σ(n) and
ϕ(n)/p + κ(n, p). Clarify if in this case the parallelization is a good
solution. Justify the answer.*

We see that the sequential portion time σ is huge, with respect to the
parallelizable part ϕ. Also, with the overhead of communication, we observe the
dominant term in the parallel time to be κ(n, p). We estimate it for p=2 and
n=32768 as:

	κ(n, p) = 4396 - 818/2 = 3987

So, in this specific example, parallelization doesn't improve the performance. In
fact, it worsens the execution time.
