import sys, os
import numpy as np

OUT_FILE = sys.argv[1]
MODEL = os.path.basename(OUT_FILE).split('.')[0]

GPUS = [1,2,4,8,16,32]
CSV_DIR = "csv"

serial_time = 0
serial_speed = 0

table = []

for gpu in GPUS:

	fn = "{}/time/{}.{}.csv".format(CSV_DIR, gpu, MODEL)
	try:
		data = np.genfromtxt(fn, delimiter=" ",
				skip_header=False)
	except IOError:
		table.append([gpu] + [np.nan]*5)
		continue

	if len(data) == 0:
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
		if work_time == 0.0:
			speedup_time = np.nan
		else:
			speedup_time = serial_time / work_time

		if speed == 0.0:
			speedup_speed = np.nan
		else:
			speedup_speed = (gpu*speed) / serial_speed

	row = [gpu, init_time, work_time, total_time, speedup_time, speedup_speed]

	table.append(row)

a = np.asarray(table)
np.savetxt(OUT_FILE, a, delimiter=" ")


#print(a)
