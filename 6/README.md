## Task 6.1
*A program that performs a matrix product  (A * B = C) parallelizing the
computation with CUDA*

The program is located in the file "1/dot.cu". The print of the final matrix was
suppressed, as it generates a enormous output.

## Task 6.2
*Timing the Kernel*

With the `nvprof` utility, a detailed log can be used to time the `dot` program.

	% nvprof ./dot
	==140328== NVPROF is profiling process 140328, command: ./dot
	==140328== Profiling application: ./dot
	==140328== Profiling result:
		    Type  Time(%)      Time     Calls       Avg       Min       Max  Name
	 GPU activities:   68.74%  45.186us         1  45.186us  45.186us  45.186us  matrixProduct(double*, double*, double*, int)
			   25.95%  17.056us         2  8.5280us  8.5120us  8.5440us  [CUDA memcpy HtoD]
			    5.31%  3.4880us         1  3.4880us  3.4880us  3.4880us  [CUDA memcpy DtoH]
	      API calls:   83.15%  462.93ms         3  154.31ms  5.7710us  462.92ms  cudaMalloc
			   15.06%  83.830ms         1  83.830ms  83.830ms  83.830ms  cudaDeviceReset
			    1.26%  7.0001ms       376  18.617us     391ns  726.01us  cuDeviceGetAttribute
			    0.33%  1.8094ms         4  452.35us  449.94us  455.77us  cuDeviceTotalMem
			    0.10%  574.59us         4  143.65us  140.49us  146.74us  cuDeviceGetName
			    0.06%  360.29us         3  120.10us  12.913us  330.92us  cudaFree
			    0.02%  98.145us         3  32.715us  26.097us  36.813us  cudaMemcpy
			    0.01%  49.897us         1  49.897us  49.897us  49.897us  cudaDeviceSynchronize
			    0.01%  46.403us         1  46.403us  46.403us  46.403us  cudaLaunch
			    0.00%  4.8940us         3  1.6310us     598ns  3.6600us  cuDeviceGetCount
			    0.00%  4.5690us         8     571ns     469ns     864ns  cuDeviceGet
			    0.00%  2.6040us         4     651ns     215ns  1.7850us  cudaSetupArgument
			    0.00%     750ns         1     750ns     750ns     750ns  cudaConfigureCall
			    0.00%     404ns         1     404ns     404ns     404ns  cudaGetLastError

We can see in the "GPU activities" section, how long the computation took
(45.186us) and how long the transfer time was. From the host to device, we sent
2 matrices, and it took 17.056us. While from the device to the host, only the
result matrix, took 3.4880us.

We also see that the cuda directive with more time was cudaMalloc, with a long
delay of 462.93ms.
