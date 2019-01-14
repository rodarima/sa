import sys
import numpy as np

MODEL = sys.argv[1]
GPUS = [1,2,4,8,16,32]
LOG_DIR = "logs"

serial_time = 0
serial_speed = 0

table = []

for gpu in GPUS:

	fn = "{}/time.{}.{}.csv".format(LOG_DIR, gpu, MODEL)
	try:
		data = np.genfromtxt(fn, delimiter=" ",
				skip_header=False)
	except IOError:
		table.append([gpu] + [np.nan]*5)
		continue

	total_time = data[0]
	init_time = data[1]
	work_time = data[2]

	speed = data[3]

	# Serial
	if gpu == 1:
		serial_time = work_time
		serial_speed = speed
		speedup_time = 1.0
		speedup_speed = 1.0
	else:
		speedup_time = serial_time / work_time
		speedup_speed = (gpu*speed) / serial_speed

	row = [gpu, init_time, work_time, total_time, speedup_time, speedup_speed]

	table.append(row)

a = np.asarray(table)
fn = "{}/{}.csv".format(LOG_DIR, MODEL)
np.savetxt(fn, a, delimiter=" ")


print(a)
