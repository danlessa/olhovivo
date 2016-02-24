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
	print(str(z_linha))
	data_mtr = filter_data(data_mtrx, cl == z_linha)
	if(len(data_mtr['t']) < 20):
		continue 
	t = data_mtr["t"]
	d = t / (60 * 60 * 24) % 7
	inds_util = ((d < 2) | (d > 4))
	inds_sab = ((d >= 2) & (d < 3))
	inds_dom = (d >= 3) & (d < 4)
	
	temp_mtr = filter_data(data_mtr, inds_util)
	if(len(temp_mtr['cl']) < 20):
		continue
	megazord2(temp_mtr)
	temp_mtr = filter_data(data_mtr, inds_sab)
	if(len(temp_mtr['cl']) < 20):
		continue
	megazord2(temp_mtr)
	temp_mtr = filter_data(data_mtr, inds_dom)
	if(len(temp_mtr['cl']) < 20):
		continue
	megazord2(temp_mtr)
	print(str(z_linha) + " done")



	
