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

The program is in 1/pi.c

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

Similarly as what was observed in the Table 4.1.

The program is in 2/pi.c

## Task 4.3
*Populate the Table 4.3 with 16 nodes and analyze the results.*

Table 4.3

|task/node|p       |runs    |mean time ms    |std time ms|
|:-------:|:------:|:------:|:--------------:|:---------:|
|1        |16      |200     |16.923951       |0.567657   |
|16       |16      |200     |16.989603       |0.478375   |

For the execution, srun was used with the number of nodes and tasks per node,
respectively:

	% srun -N 1 --ntasks-per-node 16 ./pi
	% srun -N 16 --ntasks-per-node 1 ./pi

TODO: Revise the execution time, shouldn't the first one be much higher due to
network latency?

## Task 4.4
*Compare and analyze the results from Table 4.3 and Table 4.2.*

We see that both results are very similar, with is not what we expect.

## Task 4.5
*Populate the Speedup table (Table 4.6) for this example and analyze the results.
Remark the situations for n = 65536 and p increases. Justify the behaviour of
the results.*

|n		|p	|n	|runs	|mean time ms	|std time ms	|
|:-------------:|:-----:|:-----:|:-----:|:-------------:|:-------------:|
|65536		|p	|2	|200	|0.034057	|0.002401	|
|65536		|p	|4	|200	|0.018280	|0.001952	|
|65536		|p	|8	|200	|0.011892	|0.003040	|
|65536		|p	|16	|200	|0.013553	|0.033601	|
|65536		|p	|32	|200	|0.016824	|0.010846	|
|1048576	|p	|2	|200	|0.530425	|0.009836	|
|1048576	|p	|4	|200	|0.267022	|0.003469	|
|1048576	|p	|8	|200	|0.136065	|0.004340	|
|1048576	|p	|16	|200	|0.073659	|0.005041	|
|1048576	|p	|32	|200	|0.048332	|0.012315	|
|16777216	|p	|2	|200	|8.444735	|0.010059	|
|16777216	|p	|4	|200	|4.241043	|0.113805	|
|16777216	|p	|8	|200	|2.139254	|0.182665	|
|16777216	|p	|16	|200	|1.064870	|0.010695	|
|16777216	|p	|32	|200	|0.560265	|0.152076	|
|268435456	|p	|2	|200	|135.192053	|0.245316	|
|268435456	|p	|4	|200	|67.720820	|0.434936	|
|268435456	|p	|8	|200	|33.924679	|0.431516	|
|268435456	|p	|16	|200	|17.046217	|0.429770	|
|268435456	|p	|32	|200	|8.619508	|0.458236	|



## Task 4.6 and 4.7

Task 4.5: Populate the Speedup table (Table 4.6) and the efficiencies table
(Table 4.7) for this example and analyze the results. Remark the situations for
n = 65536 and p increases. Justify the behaviour of the results.

Table 4.6 and 4.7

|p       |n       |speedup |efficiency |
|:------:|:------:|:------:|:---------:|
|2.0     |16^4    |1.938   |0.969      |
|4.0     |16^4    |3.234   |0.809      |
|8.0     |16^4    |5.654   |0.707      |
|16.0    |16^4    |5.681   |0.355      |
|32.0    |16^4    |3.956   |0.124      |
|2.0     |16^5    |1.994   |0.997      |
|4.0     |16^5    |3.906   |0.976      |
|8.0     |16^5    |7.654   |0.957      |
|16.0    |16^5    |14.321  |0.895      |
|32.0    |16^5    |21.948  |0.686      |
|2.0     |16^6    |1.979   |0.990      |
|4.0     |16^6    |3.990   |0.998      |
|8.0     |16^6    |7.986   |0.998      |
|16.0    |16^6    |15.841  |0.990      |
|32.0    |16^6    |31.025  |0.970      |
|2.0     |16^7    |1.994   |0.997      |
|4.0     |16^7    |4.005   |1.001      |
|8.0     |16^7    |8.004   |1.001      |
|16.0    |16^7    |15.969  |0.998      |
|32.0    |16^7    |31.572  |0.987      |

We can observe how the speedup increases with the number of processors. However,
the best speedup is achieved with bigger problem sizes, probably because the
overhead becomes less noticeable.

With respect to the efficiency, the best results are the ones with a bigger
problem size. A superspeedup situation happens with p=4 and p=8 with a problem
size of 16^7. It is observed that the speedup is reduced after p=8.

## Task 4.7
*According Tables 4.9 and 4.10 for this example, justify why for this
parallel version on OpenMP we can say that this parallel algorithms is strongly
scalable only for a big size problems, and for small size the algorithm does not scale.*

We see with bigger instances the efficiency is close to 1. As we can keep the
efficiency fixed with more processors, we say it is strongly scalable. On the
other hand, even if we increase the number of processors, we see the efficiency
dropping, with smaller problem sizes.


