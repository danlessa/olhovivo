
import os
import os.path
import numpy as np
from main import *

def rename(src, day, lin, tip):
	d = ""
	t = ""
	if (day == 0):
		d = "u"
	elif (day == 1):
		d = "s"
	elif (day == 2):
		d = "d"
		
	if(tip == -1):
		t = ""
	elif(tip == 0):
		t = "velhr"
	elif(tip == 1):
		t = "tript"
	elif(tip == 2):
		t = "active"
	elif(tip == 3):
		t = "mpos"
	elif(tip == 4):
		t = "mvel"
	os.rename(src, "%s-%s-%s%s.png" % (d, t, lin, t))

path = "/home/danilo_lessa/olhovivo/"
data_mtr = load_dat(path, UTC)
cl = data_mtr['cl']
lines = np.sort(np.unique(cl))
mypath = "/home/danilo_lessa/olhovivo"
pngs = []
dats = []

raw_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
raw_files.sort()
for fil in raw_files:
	if (fil[:1] == '1'):
		if (fil[-3:] == 'png'):
			pngs.append(fil)
		else:

			dats.append(fil)
i = 0
for i in range(0, len(lines)):
	j = 0
	for j in range(0, 2):
		m = 0
		for m in range(0, 4):
			rename(pngs[15*i+5*j+m], j, lines[i], m)		
	

i = 0
for i in range(0, len(lines)):
	j = 0
	for j in range(0, 2):
		rename(dats[3*i+j], j, lines[i], -1)		
