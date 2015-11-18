# -*- coding: iso-8859-15 -*-
#########################################################
'''
func.py: functional functions

Author: Danilo Lessa Bernardineli

Note: thanks for John. D. Cook for his two-point distance
script for spherical coordinates
http://www.johndcook.com/blog/python_longitude_latitude/
'''
#########################################################

#################### Dependences #########################
import numpy as np
import matplotlib.pyplot as plt
import math
import struct
import copy
import time
#################### Constants #########################
hr = 60 * 60
UTC = -2 * hr
default_matrix_config = {'x_i': -46.30, 'x_e': -46.85,
	'y_i': -23.37, 'y_e': -23.92, 'c': 125}


def check(t1, t2):
	"""
	bla
	"""
	if (t2 - t1 < 180):
		return True
	else:
		return False


def correct(data_mtr):
	"""
	blabla
	"""
	co = data_mtr["co"]
	x = data_mtr["x"]
	y = data_mtr["y"]
	cl = data_mtr["cl"]
	t = data_mtr["t"]
	v = data_mtr["v"]
	length = len(t)
	bus_qtd = np.max(np.unique(co)) + 1
	past = np.zeros(bus_qtd, dtype=np.int32)
	present = np.zeros(bus_qtd, dtype=np.int32)
	bus_set = np.zeros(bus_qtd, dtype=np.int32)

	clf = []
	cof = []
	pxf = []
	pyf = []
	tf = []
	vf = []

	for i in range(0, length):
		co_i = co[i]
		t_i = t[i]
		if(bus_set[co_i] == 0):
			past[co_i] = i
			bus_set[co_i] = 1
		else:
			if(bus_set[co_i] == 1):
				t_p = past[co_i]
				if check(t_i, t_p):
					present[co_i] = i
					bus_set[co_i] = 2
				else:
					bus_set[co_i] = 0
			else:
				if(bus_set[co_i] == 2):
					t_p = present[co_i]
					if check(t_i, t_p):
						clf.append(cl[i])
						cof.append(co[i])
						pxf.append(x[i])
						pyf.append(y[i])
						tf.append(t[i])
						vf.append(v[i])
					else:
						bus_set[co_i] = 1
						past[co_i] = i
		if i % 100000 == 0:
			print((str(length-i)))
	return {'x': pxf, 'y': pyf, 't': tf, 'v': vf, 'cl': clf, 'co': cof}


#################### Data processing functions ####################
def calc_vel_hour(data_mtr, intervalhr=2):
	"""
	Calculate median and standard deviation for given intervals in all days
	Keyword arguments:
		data_mtr -- Data matrix containing speed and time info
		intervalhr -- How much intervals per hour (default: 2)
	"""
	td = data_mtr['t']
	vd = data_mtr['v']
	v = vd
	bar_c = 24 * intervalhr
	interval = hr / intervalhr
	t = np.mod(td, hr * 24)

	stds = np.zeros(bar_c, dtype=np.float64)
	meds = np.zeros(bar_c, dtype=np.float64)
	temps = np.zeros(bar_c, dtype=np.float64)
	qtds = np.zeros(bar_c, dtype=np.int32)
	for i in range(0, bar_c):
		inds = ((t >= i * interval) & (t < (i + 1) * interval))
		meds[i] = np.median(v[inds])
		if np.isnan(meds[i]):
			meds[i] = 0
		stds[i] = np.std(v[inds])
		if np.isnan(stds[i]):
			stds[i] = 0
		temps[i] = (i * interval + (i + 1) * interval) / 2
		qtds[i] = len(v[inds])
	return {'std': stds, 'med': meds, 'tmp': temps, 'qtd': qtds}


def adjust_data(data_mtr, out=False):
	"""
	Correct raw data
	Keyword arguments:
		data_mtr -- raw data
		out -- save to file (default=false)
	"""
	cl = data_mtr['cl']
	co = data_mtr['co']
	px = data_mtr['x']
	py = data_mtr['y']
	vd = data_mtr['v']
	td = data_mtr['t']

	length = len(td)
	bus_qtd = len(np.unique(co))
	angsize = length - bus_qtd
	xf = np.zeros(angsize, dtype=np.float64)
	yf = np.zeros(angsize, dtype=np.float64)
	tf = np.zeros(angsize, dtype=np.float64)
	vf = np.zeros(angsize, dtype=np.float64)
	cof = np.zeros(angsize, dtype=np.int32)
	ang = np.zeros(angsize, dtype=np.float64)
	clf = np.zeros(angsize, dtype=np.int32)
	w = np.zeros(max(co) + 1, dtype=np.int32)
	j = 0
	for i in range(0, length):
		tco = co[i]
		if(w[tco] == 0):
			w[tco] = i
			continue
		else:
			cl1 = cl[w[tco]]
			x1 = px[w[tco]]
			y1 = py[w[tco]]
			t1 = td[w[tco]]
			v1 = vd[w[tco]]
			x2 = px[i]
			y2 = py[i]
			t2 = td[i]
			v2 = td[i]
			ang[j] = get_direction(x1, y1, x2, y2)
			xf[j] = (x1 + x2) / 2
			yf[j] = (y1 + y2) / 2
			tf[j] = (t2 + t1) / 2
			vf[j] = (v2 + v1) / 2
			cl[j] = cl1
			cof[j] = tco
			w[tco] = i
			j += 1
		if(i % 100000 == 0):
			print((length - i))

	if out is True:
		with open("adjusted-position.dat", "wb") as fid:
			length = len(tf)
			for i in range(0, length):
				fid.write(struct.pack("iiddddd", clf[i], cof[i],
					xf[i], yf[i], tf[i], vf[i], ang[i]))
				if i % 100000 == 0:
					print((str(length - i)))
	returnDict = dict()
	returnDict['x'] = xf
	returnDict['y'] = yf
	returnDict['t'] = tf
	returnDict['co'] = cof
	returnDict['cl'] = clf
	returnDict['ang'] = ang
	returnDict['v'] = vf
	return returnDict


def calc_ang_matrix(ang_mtr, matrix_config=default_matrix_config):
	"""
	Calculate a 'mean' angle contained in position square
	Keyword Arguments:
		ang_mtr -- data matrix with angles
		matrix_config -- dict with settings
	"""

	px = ang_mtr['x']
	py = ang_mtr['y']
	vd = ang_mtr['v']
	angd = ang_mtr['ang']
	x_init = matrix_config['x_i']
	x_end = matrix_config['x_e']
	y_init = matrix_config['y_i']
	y_end = matrix_config['y_e']
	c = matrix_config['length']

	deltax = math.fabs(x_end - x_init)
	deltay = math.fabs(y_end - y_init)
	intsize = 0
	if deltax > deltay:
		intsize = deltax
	else:
		intsize = deltay

	interval = intsize / (c - 1)
	ang_mtr = np.zeros((c, c), dtype=np.float64)
	q_mtr = np.zeros((c, c), dtype=np.int32)
	py_cache = []
	px_cache = []
	ang_cache = []
	v_cache = []
	for j in range(0, c):
		y_inds = ((py >= y_end + interval * j) &
				(py < y_end + interval * (j + 1)))
		py_cache.append(py[y_inds])
		px_cache.append(px[y_inds])
		ang_cache.append(angd[y_inds])
		v_cache.append(vd[y_inds])
		if(j % 100 == 0):
			print(("cache:" + str(c - j)))

	for i in range(0, c):
		for j in range(0, c):
			x_inds = ((px_cache[j] >= x_end + interval * i) &
				(px_cache[j] < x_end + interval * (i + 1)))
			if(len(px[x_inds]) < 1):
				continue
			ang_sq = ang_cache[j][x_inds]
			mcos = np.mean(np.cos(ang_sq) / v_cache[j][x_inds])
			msin = np.mean(np.sin(ang_sq) / v_cache[j][x_inds])
			mang = np.arctan2(msin, mcos)
			q_mtr[i, j] = len(ang_sq)
			ang_mtr[i, j] = mang
		if(i % 100 == 0):
			print((c - i))
	ang_mtr = np.transpose(np.fliplr(ang_mtr))
	q_mtr = np.transpose(np.fliplr(q_mtr))
	return {'matrix_ang': ang_mtr, 'matrix_qtd': q_mtr}


def calc_dif_vel_matrix(data_mtr1, data_mtr2,
	matrix_config=default_matrix_config):
	"""
	Sux
	"""
	px1 = data_mtr1['x']
	py1 = data_mtr1['y']
	vd1 = data_mtr1['v']

	px2 = data_mtr2['x']
	py2 = data_mtr2['y']
	vd2 = data_mtr2['v']

	x_init = matrix_config['x_i']
	x_end = matrix_config['x_e']
	y_init = matrix_config['y_i']
	y_end = matrix_config['y_e']
	c = matrix_config['length']

	deltax = math.fabs(x_end - x_init)
	deltay = math.fabs(y_end - y_init)
	intsize = 0
	if deltax > deltay:
		intsize = deltax
	else:
		intsize = deltay
	interval = intsize / (c - 1)
	v_mtr = np.zeros((c, c), dtype=np.float64)

	for i in range(0, c):
		for j in range(0, c):
			inds1 = ((px1 >= i * interval) & (px1 < (i + 1) * interval) &
				(py1 >= j * interval) & (py1 < (i + 1) * interval))
			inds2 = ((px2 >= i * interval) & (px2 < (i + 1) * interval) &
				(py2 >= j * interval) & (py2 < (i + 1) * interval))
			v1 = vd1[inds1]
			v2 = vd2[inds2]
			v_mtr[i, j] = (v1 - v2) / (len(v1) + len(v2))
	return v_mtr


def calc_vel_matrix(data_mtr,
	matrix_config=default_matrix_config, matrix_size=0):
	"""Calculate median speed contained in position square
	Keyword Arguments:
	data_mtr  -  -  data matrix
	matrix - config  -  -  dict with settings
	"""
	if (matrix_size < 1):
		if ('c' in matrix_config):
			c = matrix_config['c']
		else:
			c = default_matrix_config['c']
	else:
		c = matrix_size

	px = data_mtr['x']
	py = data_mtr['y']
	vd = data_mtr['v']

	x_init = matrix_config['x_i']
	x_end = matrix_config['x_e']
	y_init = matrix_config['y_i']
	y_end = matrix_config['y_e']

	deltax = math.fabs(x_end - x_init)
	deltay = math.fabs(y_end - y_init)
	intsize = 0
	if deltax > deltay:
		intsize = deltax
	else:
		intsize = deltay

	interval = intsize / (c - 1)

	v_mtr = np.zeros((c, c), dtype=np.float64)
	q_mtr = np.zeros((c, c), dtype=np.int32)
	py_cache = []
	px_cache = []
	v_cache = []
	for j in range(0, c):
		y_inds = ((py >= y_end + interval * j) &
				(py < y_end + interval * (j + 1)))
		py_cache.append(py[y_inds])
		px_cache.append(px[y_inds])
		v_cache.append(vd[y_inds])
		if(j % 100 == 0):
			print(("cache - " + str(c - j)))
	for i in range(0, c):
		for j in range(0, c):
			x_inds = ((px_cache[j] >= x_end + interval * i) &
			(px_cache[j] < x_end + interval * (i + 1)))
			if(len(px[x_inds]) < 1):
				continue
			v_sq = v_cache[j][x_inds]
			q_mtr[i, j] = len(v_sq)
			v_mtr[i, j] = np.median(v_sq)
		if(i % 100 == 0):
			print((c - i))
	v_mtr = np.transpose(np.fliplr(v_mtr))
	q_mtr = np.transpose(np.fliplr(q_mtr))
	return {'v_mtr': v_mtr, 'qtd_mtr': q_mtr}


def calc_triptime(data_mtr):
	"""
	Calculates route trip times
	Keyword arguments:
		data_mtr -- data
	"""
	cld = data_mtr['cl']
	cod = data_mtr['co']
	td = data_mtr['t']

	co = np.unique(cod)
	lengthd = len(td)

	max_co = np.max(co) + 1
	m_ti = np.zeros(max_co, dtype=np.float64)
	m_tl = np.zeros(max_co, dtype=np.float64)
	m_cl = np.zeros(max_co, dtype=np.int32)
	m_n = np.zeros(max_co, dtype=np.int32)
	times = []
	lines = []
	tis = []

	for i in range(0, lengthd):
		cl_i = cld[i]
		co_i = cod[i]
		t_i = td[i]
		clt = m_cl[co_i]
		n = m_n[co_i]
		if(cl_i != clt):
			if(n > 1):
				tt = (m_tl[co_i] - m_ti[co_i]) / 60
				if (tt > 10 and tt < 300):
					times.append(tt)
					lines.append(clt)
					tis.append(m_ti[co_i])
			m_n[co_i] = n + 1
			m_ti[co_i] = t_i
			m_cl[co_i] = cl_i
		m_tl[co_i] = t_i
		if(i % 1000000 == 0):
			print((lengthd - i))
	return {'tmp': np.array(times), 'lin': np.array(lines), 'tis': np.array(tis)}


def calc_active_bus(data_mtr, intervalhr=2):
	"""
	Calculates median active bus in given intervals
	Keyword arguments:
		data_mtr -- data
		interval hr -- how much intervals per hour (default: 2)
	"""
	td = data_mtr['t']
	cod = data_mtr['co']

	interval = hr / intervalhr
	bcount = 24 * intervalhr
	tmid = np.zeros(bcount, dtype=np.float64)
	buscount = np.zeros(bcount, dtype=np.float64)
	if(len(td) > 0):
		day = td / (24 * hr)
		modtd = np.mod(td, 24 * hr)
		min_day = math.floor(np.min(day))
		max_day = math.ceil(np.max(day))
		day_c = max_day - min_day
		for i in range(0, bcount):
			mean_array = np.zeros(day_c, dtype=np.float64)
			for j in range(0, day_c):
				d = (j + min_day)
				inds = ((modtd >= i * interval) & (modtd < (i + 1) * interval) &
					(td >= d * 24 * hr) & (td <= (d + 1) * 24 * hr))
				if(np.sum(inds) == 0):
					mean_array[j] = np.nan
				else:
					mean_array[j] = len(np.unique(cod[inds]))
			mean_array = mean_array[np.isfinite(mean_array)]
			buscount[i] = np.median(mean_array[mean_array != 0])
			tmid[i] = (i * interval + (i + 1) * interval) / 2
			if(i % 10 == 0):
				print((str(bcount - i)))
	return {'active_bus': buscount, 'tmid': tmid}


def exit_times(data_mtr):
	"""
	Calculate bus exit times based on data
	Keyword arguments:
		data_mtr -- data
	"""
	print("NI")


#################### Utility functions ####################
def dist_coord(lat1, long1, lat2, long2):
	"""
	Get distance from (x1, y1) to (x2, y2) in kilometers
	Keyword arguments:
		lat1  -  latitude of the first point
		long1  -  longitude of the first point
		lat2  -  latitude of the second point
		long2  -  longitude of the second point
	"""
	degrees_to_radians = math.pi / 180.0
	phi1 = (90.0 - lat1) * degrees_to_radians
	phi2 = (90.0 - lat2) * degrees_to_radians
	theta1 = long1 * degrees_to_radians
	theta2 = long2 * degrees_to_radians
	cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
		math.cos(phi1) * math.cos(phi2))
	arc = math.acos(cos)
	return 6371 * arc


def get_direction(x1, y1, x2, y2):
	"""
	Get angle from (x1, y1) to (x2, y2). Be careful when using near the poles
	Keyword arguments:
		x1 -- longitude of the first point
		y1 -- latitude of the first point
		x2 -- longitude of the second point
		y2 -- latitude of the second point
	"""
	dy = y2 - y1
	dx = np.cos(math.pi * y1 / 180) * (x2 - x1)
	return np.arctan2(dy, dx)


def savefig(filenamepath=0, dpip=300, inch=[6, 5]):
	"""
	Save latest figure
	Keyword arguments:
		filenamepath -- path/filename where to save
		dpip -- dpi
		inch -- inch list (default = [12, 9])
	"""
	if filenamepath == 0:
		filenamepath = str(time.time())
	fig = plt.gcf()
	fig.set_size_inches(inch[0], inch[1])
	plt.savefig(
		filenamepath +
		".png",
		dpi=dpip,
		format='png')
	plt.close()


def filter_data(data_mtr, inds):
	"""
	Filter data matrix on given indices
	"""
	filtered_mtr = copy.copy(data_mtr)
	for key in filtered_mtr:
		filtered_mtr[key] = filtered_mtr[key][inds]
	return filtered_mtr


def return_intervals(tmps, intervalhr):
	"""
	Given an array of times in seconds, this function will return
	"""
