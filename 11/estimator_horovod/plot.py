from datetime import datetime
import numpy as np
import time, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot1():
	data = np.genfromtxt("vgg19.csv", delimiter="\t", skip_header=False)
	procs = data[:,0]
	t = data[:,2]
	speedup = data[:,4]
	expected_speedup = procs
	speedup2 = data[:,5]

	plt.figure(figsize=(8, 5), dpi=120)
	fig, ax1 = plt.subplots()
	ax1.set_xlabel('GPUs')
	ax1.set_ylabel('Training time (s)')
	ax1.set_ylim((0,200))
	ax1.tick_params('y', colors='black')
	ax1.plot(procs, t, marker='o', color='black', label='Time')
	plt.legend(loc=2)

	ax2 = ax1.twinx()
	ax2.set_ylabel('Speedup')
	ax2.tick_params('y', colors='blue')
	ax2.plot(procs, expected_speedup, marker='o', color='green',label='theoretical')
	ax2.plot(procs, speedup2, marker='o', color='blue', label='with hooks')
	ax2.plot(procs, speedup, marker='o', color='red', label='with wall time')
	#plt.plot(ts, cputemp)

	#stirr = np.genfromtxt("stirr.csv")
	#for x in stirr:
	#	plt.axvline(x=x, color='red')

	#plt.yscale('log')
	#plt.xscale('log')
	plt.title('Speedup for CIFAR10 with vgg19 using Horovod')
	plt.grid(True)
	plt.legend(loc=9)

	plt.savefig("vgg19.png")
	plt.close()

def plot2():
	data = np.genfromtxt("resnet_v2_101.csv", delimiter="\t", skip_header=False)
	procs = data[:,0]
	t = data[:,2]
	speedup = data[:,4]
	expected_speedup = procs
	speedup2 = data[:,5]

	plt.figure(figsize=(8, 5), dpi=120)
	fig, ax1 = plt.subplots()
	ax1.set_xlabel('GPUs')
	ax1.set_ylabel('Training time (s)')
	ax1.set_ylim((0,200))
	ax1.tick_params('y', colors='black')
	ax1.plot(procs, t, marker='o', color='black', label='Time')
	plt.legend(loc=2)

	ax2 = ax1.twinx()
	ax2.set_ylabel('Speedup')
	ax2.tick_params('y', colors='blue')
	ax2.plot(procs, expected_speedup, marker='o', color='green',label='theoretical')
	ax2.plot(procs, speedup2, marker='o', color='blue', label='with hooks')
	ax2.plot(procs, speedup, marker='o', color='red', label='with wall time')
	#plt.plot(ts, cputemp)

	#stirr = np.genfromtxt("stirr.csv")
	#for x in stirr:
	#	plt.axvline(x=x, color='red')

	#plt.yscale('log')
	#plt.xscale('log')
	plt.title('Speedup for CIFAR10 with resnet_v2_101 using Horovod')
	plt.grid(True)
	plt.legend(loc=9)

	plt.savefig("resnet_v2_101.png")
	plt.close()

def main():

	plot1()
	plot2()

main()

