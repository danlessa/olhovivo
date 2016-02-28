
import os
import os.path
import numpy as np
from main import *

def rename(src, day, lin, tip, tds=False):
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
		
	zzz = ""
	if(tds):
		zzz="tds-"
	
	if(tip == -1):
		os.rename(src, "%s%s-%s.txt" % (zzz, d, lin))
	else:
		os.rename(src, "%s%s-%s-%s.png" % (zzz, d, t, lin))

i=0
linhas = []
linhas_ida = []
linhas_volta = []
codeFilename = "cod_linhas.csv"
mypath = "/home/danilo_lessa/olhovivo"
pngs =[]
dats =[]
if(1 == 1):
    i = 0
    with open(codeFilename, 'r') as csvfile:	
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for ro	w in csvreader:
            if(i == 2):
                i = 0
            else:
                i += 1
                linhas.append(row[0])
                if(row[2] == '1'):
                    linhas_ida.append(int(row[1]))
                if(row[2] == '2'):
                    linhas_volta.append(int(row[1]))

raw_files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
raw_files.sort()
for fil in raw_files:
	if (fil[:1] == '1'):
		if (fil[-3:] == 'png'):
			pngs.append(fil)
		else:

			dats.append(fil)

i = 0
j = 0
k = 0
ii = 0
for lin in linhas:
	for j in range(0, 3):
		rename(dats[3*i + j], j, linhas_ida[ii], -1)
		for k in range(0, 5):
			rename(pngs[15*i + 5*j + k], j, linhas_ida[ii], k)
	i += 1

	for j in range(0, 3):
		rename(dats[3*i + j], j, linhas_volta[ii], -1)
		for k in range(0, 5):
			rename(pngs[15*i + 5*j + k], j, linhas_volta[ii], k)
	i += 1
	
	for j in range(0, 3):
		rename(dats[3*i + j], j, linhas_ida[ii], -1, True)
		for k in range(0, 5):
			rename(pngs[15*i + 5*j + k], j, linhas_ida[ii], k, True)
	i += 1
