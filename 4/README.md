## Task 4.1
*Populate the Table 4.1 and analyze the results for the program that
estimates the number π.*

We slightly modified the table to include the mean and std of 200 runs,
measuring the running time of the program.

**Table 4.1** OpenMP execution time of the program that estimates the Pi number

|nr threads|runs    |mean time ms    |std time ms|
|:--------:|:------:|:--------------:|:---------:|
|2         |200     |136.260248      |0.540395   |
|4         |200     |68.743345       |1.807676   |
|8         |200     |34.402916       |2.805065   |
|16        |200     |17.196037       |0.919341   |
|32        |200     |8.641697        |0.534061   |

We can observe that with OpenMP, by increasing the number of threads used, the mean
execution time decreases significantly. 

## Task 4.2
*Populate the Table 4.2 and analyze the results for the program that estimates
the number π. Compare the results from Table 4.1 and Table 4.2.*

**Table 4.2** MPI execution time of the program that estimates the Pi number (one node)

|nr tasks|runs    |mean time ms    |std time ms|
|:------:|:------:|:--------------:|:---------:|
|2       |200     |136.010271      |1.422983   |
|4       |200     |67.964889       |0.698149   |
|8       |200     |34.164717       |1.013572   |
|16      |200     |16.987933       |0.360736   |
|32      |200     |8.511111        |0.267816   |

We see that with MPI as the number of processes *p* doubles, the average running time
almost halves.

The results are similar to what we observed in the OpenMP version
(Table 4.1). Both paradigms perform similarly for this program.

## Task 4.3
*Populate the Table 4.3 with 16 nodes and analyze the results.*

**Table 4.3** MPI execution time of the program that estimates the Pi number 
(16 nodes, one process per node)

|tasks/node|nr nodes|runs    |mean time ms    |std time ms|
|:--------:|:------:|:------:|:--------------:|:---------:|
|1         |16      |200     |16.923951       |0.567657   |

For the execution, srun was used with the number of nodes and tasks per node:

	% srun -N 16 --ntasks-per-node 1 ./pi

TODO: Revise the execution time, shouldn't the first one be much higher due to
network latency?

## Task 4.4
*Compare and analyze the results from Table 4.3 and Table 4.2.*

We see that the mean execution time with 16 nodes and 1 task per node
is very similar to the one with 1 node and 16 tasks, which is not what we expect.

TODO: confirm this analysis here.

## Task 4.5
*Populate the Speedup table (Table 4.6) for this example and analyze the results.
Remark the situations for n = 65536 and p increases. Justify the behaviour of
the results.*

**Table 4.6** Speedups for the Parallel MPI version of the trapezoidal rule for Pi number

|p \ n        |65536         |1048576       |16777216      |268435456     |
|:-----------:|:------------:|:------------:|:------------:|:------------:|
|2            |1.946         |2.014         |12.603        |2.055         |
|4            |1.685         |3.431         |24.644        |4.031         |
|6            |1.387         |5.414         |46.715        |7.925         |
|8            |0.839         |5.675         |84.618        |14.924        |

We can observe that in general the speedup increases with the number of processors.
However, in the case of *n = 65536* the speedup actually decreases when we increase *p*.
This indicates that for small problem sizes the overhead of spawning more processes is too
important compared to the parallel execution time thus decreasing the speedup.

TODO: error in the example data? seems like we get a super super speedup for *n=16777216*.

## Task 4.6
*Populate the efficiencies table (Table 4.7) for this example and analyze
the results.*

**Table 4.7** Efficiencies for the Parallel MPI version of the trapezoidal rule for Pi number

|p \ n        |65536         |1048576       |16777216      |268435456     |
|:-----------:|:------------:|:------------:|:------------:|:------------:|
|2            |0.973         |1.007         |6.302         |1.028         |
|4            |0.421         |0.858         |6.161         |1.008         |
|6            |0.231         |0.902         |7.786         |1.321         |
|8            |0.105         |0.709         |10.577        |1.865         |

A good parallelization is characterised by an efficiency close to *1*.
In this example the best results are the ones with a bigger problem size.
A super-speedup situation happens with *p=4* and *p=8* with a problem
size of *n=16777216* and *n=268435456*.

TODO: error in the example data? seems like we get a super super efficiency for *n=16777216*.

## Task 4.7
*According Tables 4.9 and 4.10 for this example, justify why for this
parallel version on OpenMP we can say that this parallel algorithms is strongly
scalable only for a big size problems, and for small size the algorithm does not scale.*

We know that a program is strongly scalable if the efficiency stays fix as we increase the 
number of processes. We can see that in this example for *n=268435456* we do indeed have a constant
efficiency (close to *1*) as we increase the number of processes.
However for smaller problem sizes if we increase the number of processes,
we see the efficiency dropping.


