#########################################################
'''
graphics.py: plots and graphics functions

Author: Danilo Lessa Bernardineli
'''
#########################################################

#################### Dependences #########################
import numpy as np
import matplotlib.pyplot as plt
from func import *


#################### Matrix maps ##########
def map_mtr(mtr, l_min=0, l_max=60, colmap='nipy_spectral'):
	"""
	Plot an matrix map
	Keyword arguments:
		mtr -- matrix to map
	"""
	fig = plt.figure()

	ax = fig.add_subplot(111)
	ax.patch.set_visible(False)
	im = plt.imread('map.png')
#	plt.imshow(im, interpolation='nearest', aspect='auto')
	cax = ax.matshow(mtr, cmap=colmap, vmin=l_min, vmax=l_max)
	plt.imshow(im, extent=cax.get_extent(), alpha=0.2)
	fig.colorbar(cax)


def map_vel(vel_matrix):
	"""
	Make matrix map
	"""
	map_mtr(vel_matrix)
	plt.title("Mapa matricial de velocidade mediana (km/h)")


#################### Plots/scatter ##########
def plot_vel_pos(data_mtr):
	"""
	Plot an velocity x position scatter plot
	Keyword arguments:
		data_mtr -- Data matrix (filtered or not)
	"""
	px = data_mtr['x']
	py = data_mtr['y']
	vd = data_mtr['v']
	color = vd

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_axis_bgcolor('black')
	plt.xlabel("Longitude (graus)")
	plt.ylabel("Latitude (graus)")
	plt.title("Mapa de velocidade (km/h)")
	plt.scatter(px, py, c=color, alpha=1, linewidth=0, cmap='nipy_spectral')
	plt.colorbar()


def plot_vel_hr(data_mtr):
	"""
	Plot an velocity x time of day (in hours) scatter plot
	Keyword arguments:
		data_mtr -- data matrix (filtered or not)
	"""
	vd = plot_mtr['v']
	td = plot_mtr['t']
	t = np.mod(td, hr * 24)

	plt.figure()
	plt.xlabel("Hora do dia(h)")
	plt.ylabel("Velocidade (km/h)")
	plt.xticks(np.arange(0, 24, 4))
	plt.title("Velocidade(km/h) x hora do dia(h)")
	plt.plot(t / hr, vd, '.', markersize=0.01)


def plot_trip_hr(trip_mtr):
	"""
	Plot an trip duration x time of day (in hours) scatter plot
	Keyword arguments:
		trip_mtr -- matrix from func.calc_triptime
	"""
	times = trip_mtr['times']
	tis = trip_mtr['tis']
	t = np.array(tis)
	t = np.mod(t, hr * 24)
	timnp = np.array(times)
	inds = ((timnp < 300) & (timnp > 0))

	plt.figure()
	plt.xlabel("Hora do dia(h)")
	plt.xticks(np.arange(0, 24, 4))
	plt.ylabel("Tempo de viagem (min)")
	plt.title("Tempo de viagens(min) x hora do dia(h)")
	plt.plot(t[inds] / hr, timnp[inds], '.', markersize=0.1)


#################### Histograms #########################
def histogram(dat, title="Histogram", bins=50):
	"""
	Generic 1D histogram routine
	Keyword arguments:
		dat -- 1D data to generate the histogram
		bins -- self-evident (default: 200)
	"""
	plt.figure()
	plt.hist(dat, bins)


def hist_vel_linha(data_mtr, bins=200):
	"""
	Generate median line speed histogram
	Keyword arguments:
		data_mtr -- Data matrix (filtered or not)
		bins -- self-evident (default: 200)
	"""
	v = data_mtr['v']
	cld = data_mtr['cld']
	cl = np.unique(cld)
	qtd = len(cl)
	vms = np.zeros(qtd, dtype=np.float64)
	for i in range(0, qtd):
		inds = (cld == cl[i])
		vms[i] = np.median(v[inds])
	histogram(vms, bins)
	plt.xlabel("Velocidade mediana (km/h)")
	plt.ylabel("Linhas")
	plt.title("Histograma de velocidades medianas nas linhas")


#################### Bars #########################
def bar_point_hr(data_mtr, intervalhr=2):
	"""
	Generate an point quantity per day hour bar graph
	Keyword arguments:
		data_mtr -- Data matrix (filtered or not)
		intervalhr -- How much intervals per hour (default: 2)
	"""
	td = data_mtr['t']
	t = np.mod(td, hr * 24)
	interval = hr / intervalhr
	bar_c = 24 * intervalhr
	temps = np.zeros(bar_c, dtype=np.float64)
	qtds = np.zeros(bar_c, dtype=np.int32)

	for i in range(0, bar_c):
		inds = ((t >= i * interval) & (t < (i + 1) * interval))
		temps[i] = (i * interval + (i + 1) * interval) / 2
		qtds[i] = len(t[inds])

	bar_hr(temps / hr, qtds)
	plt.title("Quantidade de dados por hora")
	plt.xlabel("Hora do dia")
	plt.ylabel("Dados")


def bar_trip_hr(trip_mtr):
	'''
	Write something
	'''
	times = trip_mtr["tmp"]
	tis = trip_mtr["tis"]
	tnp = np.array(times)
	tisnp = np.array(tis)
	inds = ((tnp < 300) & (tnp > 0))
	tisnp = tisnp[inds]
	tnp = tnp[inds]
	t = np.mod(tisnp, hr * 24)
	interval = 0.5 * hr
	bar_c = 24 * int(hr / interval)

	meds = np.zeros(bar_c, dtype=np.float64)
	temps = np.zeros(bar_c, dtype=np.float64)
	for i in range(0, bar_c):
		inds = ((t >= i * interval) & (t < (i + 1) * interval))
		meds[i] = np.median(tnp[inds])
		temps[i] = (i * interval + (i + 1) * interval) / 2

	bar_hr(temps / hr, meds)
	plt.xlabel("Hora do dia")
	plt.ylabel("Tempo (min)")
	plt.ylim((0, 150))
	plt.title("Tempo de viagem por hora do dia")


def bar_vel_hr(velhr_mtr):
	"""
	Generates bar plot of median speeds per day hour
	"""
	bar_hr(velhr_mtr['tmp'] / hr, velhr_mtr['med'])
	plt.title("Velocidade mediana por hora do dia")
	plt.ylim((0, 60))
	plt.xlabel("Hora do dia")
	plt.ylabel("Velocidade mediana (km/h)")


def bar_vel_hr_std(tmp, stds):
	"""
	Generates bar plot of standard deviation of speeds per day hour
	"""
	bar_hr(tmp / hr, stds)
	plt.title("Desvio padrão das velocidades por hora do dia")
	plt.ylim((0, 25))
	plt.xlabel("Hora do dia")
	plt.ylabel("Desvio padrão (km/h)")


def bar_active_hr(act_mtr):
	"""
	Write something
	"""
	bar_hr(act_mtr["tmid"] / hr, act_mtr["active_bus"])
	plt.yticks(np.arange(0, 60, 2))
	plt.ylim((0, 60))
	plt.xlabel("Hora do dia")
	plt.ylabel("Mediana de ônibus ativos")
	plt.title("Mediana da quantidade de ônibus ativos por hora do dia")


def bar_hr(tdat, dat):
	"""
	Generic bar plot of ~something~ on a day time interval ([0h, 24h])
	Keyword arguments:
		tdat -- time data
		dat -- data
	"""
	width = 0.3
	plt.figure()
	plt.xticks(np.arange(0, 24, 2))
	plt.yticks(np.arange(0, 150, 5))
	plt.ylim((0, 65))
	plt.xlim((0, 24))
	plt.grid(True)
	plt.bar(tdat, dat, width)
