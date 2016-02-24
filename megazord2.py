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

z_linhas = np.unique(data_mtr["cl"])

for z_linha in z_linhas:
	data_mtr = data_mtrx[data_mtrx["cl"] == z_linha]
	d = t / (60 * 60 * 24) % 7
	inds_util = ((d < 2) | (d > 4))
	inds_sab = ((d >= 2) & (d < 3))
	inds_dom = (d >= 3) & (d < 4)

	megazord2(data_mtr[data_mtr['t'] == inds_util])
	megazord2(data_mtr[data_mtr['t'] == inds_sab])
	megazord2(data_mtr[data_mtr['t'] == inds_dom])



	
