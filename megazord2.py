# -*- coding: utf-8 -*-
### megazord2: para gerar linhas individuais

#dependências iniciais e constantes
import numpy as np
import matplotlib as plt
import scipy.stats
from main import *
from func import *
from graphics import *
from helper import *

path = "/home/danilo_lessa/olhovivo/"
#carregamento dos dados
data_mtrx = load_dat(path, UTC)

cl = data_mtrx["cl"]
z_linhas = np.unique(cl)

for z_linha in z_linhas:
	data_mtr = filter_data(data_mtrx, cl == z_linha)
	if(len(data_mtr['t']) == 0):
		continue 
	t = data_mtr["t"]
	d = t / (60 * 60 * 24) % 7
	inds_util = ((d < 2) | (d > 4))
	inds_sab = ((d >= 2) & (d < 3))
	inds_dom = (d >= 3) & (d < 4)

	megazord2(filter_data(data_mtr, t == inds_util))
	megazord2(filter_data(data_mtr, t == inds_sab))
	megazord2(filter_data(data_mtr, t == inds_dom))



	
