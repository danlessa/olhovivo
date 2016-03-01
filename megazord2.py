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
    filestr = "u-"+str(z_linha)
    megazord2(temp_mtr, trip_t_mtr, z_linha, filestr)


    trip_t_mtr = filter_data(trip_mtr, inds_t_sab)
    temp_mtr = filter_data(data_mtr, inds_sab)
    filestr = "s-"+str(z_linha)
    megazord2(temp_mtr, trip_t_mtr, z_linha, filestr)

    trip_t_mtr = filter_data(trip_mtr, inds_t_dom)
    temp_mtr = filter_data(data_mtr, inds_dom)
    filestr = "d-"+str(z_linha)
    megazord2(temp_mtr, trip_t_mtr, z_linha, filestr)
    print(str(z_linha) + " done")
    
    
def linhagentd(z_linha1, z_linha2):
    print(str(z_linha1))
    inds1 = (cl == z_linha1)
    inds2 = (cl == z_linha2)
    inds = inds1 | inds2
    data_mtr = filter_data(data_mtrx, inds)
    t = data_mtr["t"]
    d = t / (60 * 60 * 24) % 7
    inds_util = ((d < 2) | (d > 4))
    inds_sab = ((d >= 2) & (d < 3))
    inds_dom = (d >= 3) & (d < 4)
    
    c_trip = trip_mtr['lin']
    t_trip = trip_mtr['tmp']
    d = t_trip / (60 * 60 * 24) % 7
    indt1 = c_trip == z_linha1
    indt2 = c_trip == z_linha2
    indt = indt1 | indt2
    inds_t = indt
    inds_t_util = ((d < 2) | (d > 4)) & inds_t
    inds_t_sab = ((d >= 2) & (d < 3)) & inds_t
    inds_t_dom = (d >= 3) & (d < 4) & inds_t

    trip_t_mtr = filter_data(trip_mtr, inds_t_util)
    temp_mtr = filter_data(data_mtr, inds_util)
    filestr = "tds-u-"+str(z_linha1)
    megazord2(temp_mtr, trip_t_mtr, z_linha1, filestr)

    trip_t_mtr = filter_data(trip_mtr, inds_t_sab)
    temp_mtr = filter_data(data_mtr, inds_sab)
    filestr = "tds-s-"+str(z_linha1)
    megazord2(temp_mtr, trip_t_mtr, z_linha1, filestr)

    trip_t_mtr = filter_data(trip_mtr, inds_t_dom)
    temp_mtr = filter_data(data_mtr, inds_dom)
    filestr = "tds-d-"+str(z_linha1)
    megazord2(temp_mtr, trip_t_mtr, z_linha1, filestr)
    print(str(z_linha1) + " done")

codeFilename = "cod_linhas.csv"
linhas = {}

if(1 == 1):
    with open(codeFilename, 'r') as csvfile:    
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            linha = row[0]
            if(linha not in linhas):
                linhas[linha] = {}
                linhas[linha]['ida'] = -1
                linhas[linha]['volta'] = -1
            if(row[2] == '1'):
                linhas[linha]['ida'] = int(row[1])
            if(row[2] == '2'):
                linhas[linha]['volta'] = int(row[1])

path = "/home/danilo/olhovivo/"
#carregamento dos dados
data_mtrx = load_dat(path, UTC)
cl = data_mtrx["cl"]
trip_mtr = calc_triptime(data_mtrx)

for lin in linhas:
    linha = linhas[lin]
    hasIda = False
    hasVolta = False
    if linha['ida'] != -1:
        linhagen(linha['ida'])
        hasIda = True
    if linha['volta'] != -1:
        linhagen(linha['volta'])
        hasVolta = True
    if (hasIda and hasVolta):
        print(linha['volta'])
        linhagentd(linha['ida'], linha['volta'])
    elif hasIda:
        print("sux")
        linhagentd(linha['ida'], linha['ida'])
    elif hasVolta:
        print("suxx")
        linhagentd(linha['volta'], linha['volta'])

    
