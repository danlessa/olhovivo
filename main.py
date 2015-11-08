#########################################################
'''
main.py: funções de rotina

Author: Danilo Lessa Bernardineli
'''
#########################################################

################### Dependências #########################
import numpy as np
import csv
import os
import time
import struct
import glob
import os
from func import *

################### Constantes globais #########################
dat_path = os.getcwd()
csv_filename = "cod_linhas.dat"


################### Rotina de inicialização ###################
def main():
	"""
	Script for processing municipal bus data from São Paulo
	"""
	print("Inicializando")
	data_mtr = load_dat(dat_path)
	print("Calculando tempos de viagem")
	trip_mtr = calc_triptime(data_mtr)
	print("Pronto!")


################### Data init ###################
def ready_data(data_mtr):
	"""
	Process raw data to get trip times and speed interval matrix
	"""

	return None


################### Rotinas de processamento filtrado ###################
def proc_geral():
	"""
	General (everything together) processing routine
	"""
	
	
	print("Not implemented")


def proc_util():
	"""
	Work days processing routine
	"""
	print("Not implemented")


def proc_fds():
	"""
	Weekends processing routine
	"""
	print("Not implemented")


def proc_peak():
	"""
	Peak times processing routine
	"""
	print("Not implemented")


def proc_zone():
	"""
	Zonal processing routine
	"""
	print("Not implemented")


################### Rotinas de carregamento ###################
def load_dat(path, utc, all=False):
	"""
	Loads data from some file,  while correcting the time for UTC
	Keyword arguments:
		path  -  -  path to folder containing dat files
		utc  -  -  UTC correction in seconds
		all -- retrive all data (default=false)
	"""

	listFiles = glob.glob(os.path.join(path, "posicoes*.dat"))
	filesCount = len(listFiles)
	clf = np.array(0, dtype=np.int32)
	cof = np.array(0, dtype=np.int32)
	xf = np.array(0, dtype=np.float64)
	yf = np.array(0, dtype=np.float64)
	tf = np.array(0, dtype=np.float64)
	vf = np.array(0, dtype=np.float64)

	for i in range(0, filesCount):
		filename = listFiles[i]
		print(("Loading file " + str(i) + "/" + str(filesCount)))
		size = os.path.getsize(filename)
		length = int((size - size % 40) / 40)
		cl = np.zeros(length, dtype=np.int32)
		co = np.zeros(length, dtype=np.int32)
		x = np.zeros(length, dtype=np.float64)
		y = np.zeros(length, dtype=np.float64)
		t = np.zeros(length, dtype=np.float64)
		v = np.zeros(length, dtype=np.float64)
		print((str(length)))
		t1 = time.time()
		with open(filename, "rb") as fid:
			for i in range(0, length):
				cl[i], co[i], x[i], y[i], t[i], v[
					i] = struct.unpack('iidddd', fid.read(40))
				if i % 1000000 == 0:
					print((str(length - i)))
		t2 = time.time()
		print((str(t2 - t1)))
		print((str(length)))
		clf = np.append(clf, cl)
		cof = np.append(cof, co)
		xf = np.append(xf, x)
		yf = np.append(yf, y)
		tf = np.append(tf, t)
		vf = np.append(vf, v)

	inds = (vf == vf)
	if all is False:
		inds = (((vf < 70) & (vf > 3)))
	clf = clf[inds]
	cof = cof[inds]
	xf = xf[inds]
	yf = yf[inds]
	tf = tf[inds] + utc
	vf = vf[inds]
	return {'cl': clf, 'co': cof, 'x': xf, 'y': yf, 't': tf, 'v': vf}


def load_adj_dat(filename):
	"""
	Loads data from some file,  while correcting the time for UTC
	Keyword arguments:
		path  -  -  path to folder containing dat files
		utc  -  -  UTC correction in seconds
	"""
	size = os.path.getsize(filename)
	length = int((size - size % 48) / 48)
	cl = np.zeros(length, dtype=np.int32)
	co = np.zeros(length, dtype=np.int32)
	x = np.zeros(length, dtype=np.float64)
	y = np.zeros(length, dtype=np.float64)
	t = np.zeros(length, dtype=np.float64)
	v = np.zeros(length, dtype=np.float64)
	ang = np.zeros(length, dtype=np.float64)
	print((str(length)))
	t1 = time.time()
	with open(filename, "rb") as fid:
		for i in range(0, length):
			cl[i], co[i], x[i], y[i], t[i], v[i
				], ang[i] = struct.unpack('iiddddd', fid.read(48))
			if i % 1000000 == 0:
				print((str(length - i)))
	t2 = time.time()
	print((str(t2 - t1)))
	print((str(length)))
	return {'cl': cl, 'co': co, 'x': x, 'y': y, 't': t, 'v': v}


def load_cod(filename):
	"""
	Load bus line codes and bus internal codes from CSV file
	Keyword arguments:
		filename  -  -  path to csv file
	"""
	cod_pub = []
	cod_int = []
	direction = []
	circula = []
	with open(filename, 'r') as fid:
		reader = csv.reader(fid, delimiter=', ')
		for row in reader:
			cod_pub.append(row[0])
			cod_int.append(int(row[1]))
			direction.append(int(row[2]))
			circula.append(bool(row[3]))
	return {'cp': cod_pub, 'cl': cod_int, 'di': direction, 'ci': circula}

#################### Misc #########################
if __name__ == "__main__":
	main()
