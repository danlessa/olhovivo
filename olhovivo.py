# -*- coding: iso-8859-15 -*-

#########################################################
'''
olhovivo.py: Data acquisition scripts

Author: Danilo Lessa Bernardineli
'''
#########################################################

#################### Dependences #########################
import time
import csv
import struct
import math
import os
import glob
from olhovivo.wrap import *


#################### routine #########################
def main():
	"""
	Run script
	"""
	TOKEN = "ab0855f97de16ac2b98e82920f6f07b1539ec2fc666d2b559303011bb057a25a"
	POSICOES = "posicoes.dat"
	COD_LINHAS = "cod_linhas.csv"
	dic_bus = dict()

	linhas = scriptCarregarCodigos(COD_LINHAS)

	if(os.path.exists(POSICOES)):
		c = len(glob.glob("*.dat"))
		os.rename(POSICOES, "posicoes-" + str(c) + ".dat")

	while 1 == 1:
		with open(POSICOES, "ab") as fil:
			t1 = time.time()
			scriptDumpPos(fil, linhas, TOKEN, dic_bus)
			t2 = time.time()
			delta = t2 - t1
			if(delta < 60 * 3):
				time.sleep(60 * 3 - delta)


#################### Data acquistion #########################
def scriptObterCodigos(arquivo, tripfile, aut):
	"""
	Get internal line codes and store at an CSV file
	Keyword arguments:
		arquivo -- file to store the internal codes
		tripfiles -- GTFS file to get the public line codes
		aut -- auth request
	"""
	linhas = []

	with open(tripfile) as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		next(spamreader)
		for row in spamreader:
			if(row[4] != "1"):
				linhas.append(row[0].strip('\"'))

	t1 = time.time()
	with open(arquivo, "w", newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=",")
		for line in linhas:
			bl = buscarLinhas(line, aut)
			for hehe in bl:
				csvwriter.writerow([line, hehe["CodigoLinha"],
					hehe["Sentido"], hehe["Circular"]])
	t2 = time.time()
	print(("time: " + str(t2 - t1)))
	print(("iter: " + str(len(linhas))))


def scriptCarregarCodigos(arquivo):
	"""Load internal line codes from a CSV file made by the previous function
	Keyword arguments:
		arquivo -- CSV filepath
	"""
	lines = []
	with open(arquivo) as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for line in csvreader:
			lines.append(line)
	return lines


def setDictBus(dictbus, i, code, p, px, py, t, cz, v):
	"""
	Update bus dictionary
	"""
	dictbus[i][0] = code
	dictbus[i][1] = p
	dictbus[i][2] = px
	dictbus[i][3] = py
	dictbus[i][4] = t
	dictbus[i][5] = cz
	dictbus[i][6] = v


def dist_coord(lat1, long1, lat2, long2):
	"""
	Get distance from (x1, y1) to (x2, y2) in kilometers
	Keyword arguments:
		lat1  -  latitude of the first point
		long1  -  longitude of the first point
		lat2  -  latitude of the second point
		long2  -  longitude of the second point
	"""

	# Convert latitude and longitude to
	# spherical coordinates in radians.
	degrees_to_radians = math.pi / 180.0

	# phi = 90 - latitude
	phi1 = (90.0 - lat1) * degrees_to_radians
	phi2 = (90.0 - lat2) * degrees_to_radians

	# theta = longitude
	theta1 = long1 * degrees_to_radians
	theta2 = long2 * degrees_to_radians

	# Compute spherical distance from spherical coordinates.

	# For two locations in spherical coordinates
	# (1, theta, phi) and (1, theta', phi')
	# cosine( arc length ) =
	#	sin phi sin phi' cos(theta-theta') + cos phi cos phi'
	# distance = rho * arc length

	cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
		math.cos(phi1) * math.cos(phi2))
	arc = math.acos(cos)

	# Remember to multiply arc by the radius of the earth
	# in your favorite set of units to get length.  (km)
	return 6371 * arc


def scriptDumpPos(arquivo, linhas, tok, dic_bus):
	"""
	Dump bus positions in a binary file
	Keyword arguments:
		arquivo -- filepath
		linhas -- return from scriptCarregarCodigos
		tok -- API access token
		dic_bus -- bus dict
	"""
	aut = autenticar(tok)
	for line in linhas:
		code = line[1]
		jt = returnPosicao(code, aut)
		t2 = time.time()

		if(not isinstance(jt, dict)):
			aut = autenticar(tok)
			print("zzz")
			continue
		if(len(jt) != 2):
			continue

		vs = jt["vs"]
		for bus in vs:
			p = bus["p"]
			px = bus["px"]
			py = bus["py"]

			if(p not in dic_bus):
				dic_bus[p] = [None] * 7
				setDictBus(dic_bus, p, code, p, px, py, t2, 0, -1)
			else:
				cz = dic_bus[p][5]

				past_code = dic_bus[p][0]
				past_px = dic_bus[p][2]
				past_py = dic_bus[p][3]
				past_t = dic_bus[p][4]
				past_cz = dic_bus[p][5]
				past_v = dic_bus[p][6]

				v = 0
				if(px == past_px and py == past_py):
					if(cz == 1):
						setDictBus(dic_bus, p, code, p, px, py, t2, 1, v)
						continue
					else:
						cz = 1
				else:
					v = 60 * 60 * \
						dist_coord(py, px, past_py, past_px) / (t2 - past_t)
					cz = 0

				arquivo.write(
					struct.pack(
						"iidddd",
						int(past_code),
						int(p),
						float(past_px),
						float(past_py),
						float(past_t),
						float(past_v)))
				setDictBus(dic_bus, p, code, p, px, py, t2, cz, v)


if __name__ == "__main__":
	main()
