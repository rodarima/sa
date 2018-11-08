import numpy as np

data = np.genfromtxt('times.csv', delimiter=',')

# Skip header
data = data[1:]

print("p\tn\tspeedup\tefficiency")

for row in data:
	p,n,runs,tmean,tstd = row
	if p == 1:
		Ts = tmean
	else:
		Tp = tmean
		speedup = Ts/Tp
		power = int(np.log(n)/np.log(16))
		eff = speedup / p
		print("{}\t16^{}\t{:.3f}\t{:.3f}".format(p, power, speedup, eff))

