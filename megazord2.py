# -*- coding: utf-8 -*-
### megazord2: para gerar linhas individuais

#dependências iniciais e constantes
import matplotlib as mpl
mpl.use('Agg')

import numpy as np
import matplotlib as plt
import scipy.stats
from main import *
from func import *
from graphics import *
from helper import *

def linhagen(z_linha):
	print(str(z_linha))
	data_mtr = filter_data(data_mtrx, cl == z_linha)
	t = data_mtr["t"]
	d = t / (60 * 60 * 24) % 7
	inds_util = ((d < 2) | (d > 4))
	inds_sab = ((d >= 2) & (d < 3))
	inds_dom = (d >= 3) & (d < 4)
	
	c_trip = trip_mtr['lin']
	t_trip = trip_mtr['tmp']
	d = t_trip / (60 * 60 * 24) % 7
	inds_t = (c_trip == z_linha)
	inds_t_util = ((d < 2) | (d > 4)) & inds_t
	inds_t_sab = ((d >= 2) & (d < 3)) & inds_t
	inds_t_dom = (d >= 3) & (d < 4) & inds_t

	trip_t_mtr = filter_data(trip_mtr, inds_t_util)
	temp_mtr = filter_data(data_mtr, inds_util)
	megazord2(temp_mtr, trip_t_mtr, z_linha)

	trip_t_mtr = filter_data(trip_mtr, inds_t_sab)
	temp_mtr = filter_data(data_mtr, inds_sab)
	megazord2(temp_mtr, trip_t_mtr, z_linha)

	trip_t_mtr = filter_data(trip_mtr, inds_t_dom)
	temp_mtr = filter_data(data_mtr, inds_dom)
	megazord2(temp_mtr, trip_t_mtr, z_linha)
	print(str(z_linha) + " done")
	
	
def linhagentd(z_linha1, z_linha2):
	print(str(z_linha))
	data_mtr = filter_data(data_mtrx, (cl == z_linha1 or cl ==z_linha2))
	t = data_mtr["t"]
	d = t / (60 * 60 * 24) % 7
	inds_util = ((d < 2) | (d > 4))
	inds_sab = ((d >= 2) & (d < 3))
	inds_dom = (d >= 3) & (d < 4)
	
	c_trip = trip_mtr['lin']
	t_trip = trip_mtr['tmp']
	d = t_trip / (60 * 60 * 24) % 7
	inds_t = (c_trip == z_linha1 or c_trip == z_linha2)
	inds_t_util = ((d < 2) | (d > 4)) & inds_t
	inds_t_sab = ((d >= 2) & (d < 3)) & inds_t
	inds_t_dom = (d >= 3) & (d < 4) & inds_t

	trip_t_mtr = filter_data(trip_mtr, inds_t_util)
	temp_mtr = filter_data(data_mtr, inds_util)
	megazord2(temp_mtr, trip_t_mtr, z_linha)

	trip_t_mtr = filter_data(trip_mtr, inds_t_sab)
	temp_mtr = filter_data(data_mtr, inds_sab)
	megazord2(temp_mtr, trip_t_mtr, z_linha)

	trip_t_mtr = filter_data(trip_mtr, inds_t_dom)
	temp_mtr = filter_data(data_mtr, inds_dom)
	megazord2(temp_mtr, trip_t_mtr, z_linha)
	print(str(z_linha) + " done")


path = "/home/danilo_lessa/olhovivo/"
#carregamento dos dados
data_mtrx = load_dat(path, UTC)

cl = data_mtrx["cl"]
z_linhas = np.unique(cl)

trip_mtr = calc_triptime(data_mtrx)

i=0
line

linhas = []
linhas_ida = []
linhas_volta = []

if(1 == 1):
    i = 0
    with open(codeFilename, 'r') as csvfile:	
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            if(i == 2):
                i = 0
            else:
                i += 1
                linhas.append(row[0])
                if(row[2] == '1'):
                    linhas_ida.append(int(row[1]))
                if(row[2] == '2'):
                    linhas_volta.append(int(row[1]))

i = 0
for z_linha in linhas:
	linhagen(linhas_ida[i])
	linhagen(linhas_volta[i])
	linhagentd(linhas_ida[i], linhas_volta[i])
	i += 1



	
