from datetime import datetime
import numpy as np
import time, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

LOG_DIR = "logs"
GPUS = [1,2,4,8,16,32]
MODELS = ["resnet_v2_101", "vgg19", "inception_v4"]

def plot_speedup(model):
	fn = "{}/{}.csv".format(LOG_DIR, model)
	data = np.genfromtxt(fn, delimiter=" ", skip_header=False)
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
	ax1.set_xlim((1,32))
	ax1.tick_params('y', colors='black')
	ax1.plot(procs, t, marker='o', color='black', label='Time')
	plt.legend(loc=2)

	ax2 = ax1.twinx()
	ax2.set_ylabel('Speedup')
	ax2.set_ylim((0,32))
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
	plt.title('Speedup for CIFAR10 with {} using Horovod'.format(model))
	plt.grid(True)
	plt.legend(loc=9)

	plt.savefig("fig/{}.png".format(model))
	plt.close()

def get_efficiency(model):
	fn = "{}/{}.csv".format(LOG_DIR, model)
	data = np.genfromtxt(fn, delimiter=" ", skip_header=False)
	procs = data[:,0]
	t = data[:,2]
	speedup_time = data[:,4]
	speedup_speed = data[:,5]

	efficiency_time = speedup_time / procs
	efficiency_speed = speedup_speed / procs

	return (efficiency_time, efficiency_speed)

def plot_efficiency_dict(eff, name):
	fig, ax1 = plt.subplots(figsize=(8, 4), dpi=120)
	ax1.set_xlabel('GPUs')
	ax1.set_ylabel('Efficiency')
	ax1.set_xlim((1,32))

	for model in MODELS:
		ax1.plot(GPUS, eff[model], marker='o', label=model)

	plt.legend(loc=2)

	plt.xscale('log')
	plt.xticks(GPUS, GPUS)
	plt.title('Efficiency using {}'.format(name))
	plt.grid(True)
	plt.legend(loc=9)

	plt.savefig("fig/efficiency_{}.png".format(name))
	plt.close()

def plot_efficiency(models):

	eff_time = {}
	eff_speed = {}

	for model in models:
		eff_time[model], eff_speed[model] = get_efficiency(model)

	plot_efficiency_dict(eff_time, "time")
	plot_efficiency_dict(eff_speed, "speed")

def main():


	#for model in models:
	#	plot_model(model)

	plot_efficiency(MODELS)

main()

