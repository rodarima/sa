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
