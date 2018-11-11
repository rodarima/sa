## Task 5.1

*Analize with your partner both codes 5.1 and 5.2 that implement a matrix-
vector multiplication. Write in the report of this laboratory the main
differences of both codes.*

The main difference is that the sequential program does all the operations
sequentially, while the parallel code distributes the work among different
processes, and then computes the work in parallel.

The parallelization of the matrix vector product is done by scattering across
the processors the rows of the matrix A in groups, along the vector, in order
to compute the product.


