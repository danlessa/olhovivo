# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from func import *
from graphics import *
from main import *


def vel_analyze(data_mtr, inds, suptitle):
	"""
	Standard speed analysis routine
	"""
	mtr = filter_data(data_mtr, inds)
	vel_hour = calc_vel_hour(mtr)
	bar_vel_hr(vel_hour)
	plt.suptitle(suptitle)
	savefig()


def active_analyze(data_mtr, ind, suptitle):
	"""
	Standard active bus analysis routine
	"""
	mtr = filter_data(data_mtr, ind)
	active_mtr = calc_active_bus(mtr)
	bar_active_hr(active_mtr)
	plt.suptitle(suptitle)
	savefig()


def interval_analyze(data_mtr, inds, suptitle, matrix_size):
	"""
	Write something
	"""
	mtr = filter_data(data_mtr, inds)
	vdata = calc_vel_matrix(mtr, default_matrix_config, matrix_size)
	v_mtr = vdata['v_mtr']
	q_mtr = vdata['qtd_mtr']

	map_vel(v_mtr)
	plt.suptitle(suptitle)
	savefig()
	qtd = np.sum(q_mtr)
	map_mtr(q_mtr / qtd, 0, 0.003)
	plt.suptitle(suptitle)
	plt.title("Distribuição normalizada")
	savefig()


def dif_analyze(data_mtr, ind1, ind2, matrix_size, dif_size, suptitle):
	"""
	Write something
	"""
	vmtr1 = filter_data(data_mtr, ind1)
	vmtr2 = filter_data(data_mtr, ind2)
	vdata1 = calc_vel_matrix(vmtr1,
	default_matrix_config, matrix_size)
	vdata2 = calc_vel_matrix(vmtr2,
	default_matrix_config, matrix_size)
	dif_mtr = vdata1['v_mtr'] - vdata2['v_mtr']
	map_mtr(dif_mtr, -dif_size, dif_size, 'seismic')
	plt.suptitle(suptitle)
	savefig()


def zone_analyze(data_mtr, matrix_config, suptitle):
	"""
	Write something
	"""
	y_i = matrix_config['y_i']
	y_e = matrix_config['y_e']
	x_i = matrix_config['x_i']
	x_e = matrix_config['x_e']
	px = data_mtr['x']
	py = data_mtr['y']

	#isolando dados
	inds_zone = ((px < x_i) & (px > x_e) & (py < y_i) & (py > y_e))
	zone_mtr = filter_data(data_mtr, inds_zone)

	#distribuiçao de velocidades
	vel_analyze(data_mtr, inds_zone, suptitle)

	#onibus ativos
	active_mtr = calc_active_bus(zone_mtr)
	bar_active_hr(active_mtr)
	plt.yticks(np.arange(0, 7000, 500))
	plt.ylim((0, 7000))
	plt.suptitle(suptitle)
	savefig()

	#distribuição normalizada e velocidades medianas
	v_matrix = calc_vel_matrix(zone_mtr, matrix_config)
	map_vel(v_matrix['v_mtr'])
	plt.suptitle(suptitle)
	savefig()
	map_mtr(v_matrix['qtd_mtr'] / np.sum(v_matrix['qtd_mtr']), 0, 0.005)
	plt.suptitle(suptitle)
	savefig()

	cl = zone_mtr['cl']
	inds_ida = (cl < 15000)
	inds_volta = (cl > 15000)
	dif_bar_analyze(zone_mtr, inds_ida, inds_volta,
	"Diferença ida x volta - " + suptitle)

	#
	t = data_mtr['t']
	cl = data_mtr['cl']
	h = (t % 24)

	#matinal
	manha_inds = (h > 7.5) & (h < 8.5)
	manha_ida_inds = manha_inds & (cl < 15000)
	manha_volta_inds = manha_inds & (cl > 15000)
	manha_ida_mtr = filter_data(data_mtr, manha_ida_inds)
	manha_volta_mtr = filter_data(data_mtr, manha_volta_inds)
	manha_ida_vdata = calc_vel_matrix(manha_ida_mtr, matrix_config)
	manha_volta_vdata = calc_vel_matrix(manha_volta_mtr, matrix_config)
	manha_dif_mtr = manha_ida_vdata['v_mtr'] - manha_volta_vdata['v_mtr']
	map_mtr(manha_dif_mtr, -5, 5, 'seismic')
	plt.suptitle(suptitle + " - pico matinal - diferença ida vs volta")
	savefig()

	#vespertino
	tarde_inds = (h > 17.5) & (h < 18.5)
	tarde_ida_inds = tarde_inds & (cl < 15000)
	tarde_volta_inds = tarde_inds & (cl > 15000)
	tarde_ida_mtr = filter_data(data_mtr, tarde_ida_inds)
	tarde_volta_mtr = filter_data(data_mtr, tarde_volta_inds)
	tarde_ida_vdata = calc_vel_matrix(tarde_ida_mtr, matrix_config)
	tarde_volta_vdata = calc_vel_matrix(tarde_volta_mtr, matrix_config)
	tarde_dif_mtr = tarde_ida_vdata['v_mtr'] - tarde_volta_vdata['v_mtr']
	map_mtr(tarde_dif_mtr, -5, 5, 'seismic')
	plt.suptitle(suptitle + " - pico vespertino - diferença ida vs volta")
	savefig()


def trip_analyze(data_mtr, inds, suptitle):
	"""
	aaaa
	"""
	mtr = filter_data(data_mtr, inds)
	bar_trip_hr(mtr)
	plt.suptitle(suptitle)
	savefig()


def dif_bar_analyze(data_mtr, ind1, ind2, suptitle):
	"""
	wads
	"""
	mtr1 = filter_data(data_mtr, ind1)
	mtr2 = filter_data(data_mtr, ind2)
	v1_hour = calc_vel_hour(mtr1)
	v2_hour = calc_vel_hour(mtr2)
	dif_vel_hour = v1_hour['med'] - v2_hour['med']

	bar_hr(v1_hour['tmp'] / hr, dif_vel_hour)
	plt.title("Velocidade mediana por hora do dia")
	plt.xlabel("Hora do dia")
	plt.ylabel("Velocidade mediana (km/h)")

	plt.ylim((-10, 10))
	plt.yticks(np.arange(-10, 10, 2))
	plt.suptitle(suptitle)
	savefig()