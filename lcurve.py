import numpy as np
import math
import matplotlib.pyplot as plt
import sys
import csv
from scipy.optimize import curve_fit
filename = 'lcurvePoints.csv'
fields = []
rows = []
fig = plt.figure()
ax = fig.add_subplot(111)
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)

def timeconv(string):
    temp = string
    hh, mm, ss = list(map(float, temp.split(':')))
    if (hh < 12): hh += 24
    return hh + mm/60 + ss/3600

x, y, z, mag = [np.empty(0) for i in range(4)]

for row in rows:
    rowstr = row[0]
    x0, y0, z0, rat  = rowstr.split()
    x0 = timeconv(x0); y0 = float(y0); z0 = float(z0)
    x = np.append(x, x0); y = np.append(y, y0)                                             
    rat = z0 / y0
    mag0 = -2.5 * math.log10(rat)
    mag = np.append(mag, mag0)

def func(x, a, b, c, d):
    return a * np.sin(b + c*x) + d

x -= x[0]
xnew = np.linspace(x[0], x[-1], 300)

param, pcov = curve_fit(func, x, mag)
#print(param)
ynew = func(xnew, *param)
plt.scatter(x, mag)
plt.plot(xnew, ynew)
plt.suptitle("Light curve of Vesta", fontweight='bold')

ax.set_title(f'Period of rotation: {round(2 * math.pi/param[2], 1)}hours')

plt.ylabel('Relative magnitude')
plt.xlabel('Time in hours')
plt.show()

