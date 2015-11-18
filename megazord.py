# -*- coding: utf-8 -*-
#dependências iniciais e constantes
import numpy as np
import matplotlib as plt
import scipy.stats
from main import *
from func import *
from graphics import *
from helper import *
path = "/home/danilo/olhovivo/data/"
#carregamento dos dados
data_mtr = load_dat(path, UTC)
#declaracoes iniciais
t = data_mtr['t']
d = t / (60 * 60 * 24) % 7
cl = data_mtr['cl']
h = (t % 24)

print("1")
#indices
inds_all = (t == t)

del t

inds_util = ((d < 2) | (d > 4))
inds_sab = ((d >= 2) & (d < 3))
inds_fds = (d >= 2) & (d < 4)
inds_dom = (d >= 3) & (d < 4)
print("2")

del d

#Parte 1 - Distribuição de velocidades

print("parte 1")
#barras de velocidades geral
vel_analyze(data_mtr, inds_all, "Geral")

#barras de velocidades em dias uteis
vel_analyze(data_mtr, inds_util, "Dias úteis")

#barras de velocidades nos sábados
vel_analyze(data_mtr, inds_sab, "Sábados")

#barras de velocidades nos domingos
vel_analyze(data_mtr, inds_dom, "Domingos")

#Parte 2 - Distribuição de tempos de viagem
print("parte 2")
trip_mtr = calc_triptime(data_mtr)
ti = trip_mtr['tis']
dt = ti / (60 * 60 * 24) % 7
#histograma de tempos de viagem
plt.hist(trip_mtr["tmp"], bins=100, range=(0, 300))
plt.xlabel("Tempo de viagem (min)")
plt.ylabel("Quantidade de viagens")
plt.suptitle("Geral")
plt.title("Distribuição dos tempos de viagens")
savefig()
#barras de tempos de viagem geral
bar_trip_hr(trip_mtr)
plt.suptitle("Geral")
savefig()
#barras de tempos de viagem em dias utéis
ind_util = ((dt < 2) | (dt > 4))
trip_analyze(trip_mtr, ind_util, "Dias úteis")
#barras de tempos de viagem nos sábados
ind_sab = ((dt >= 2) & (dt < 3))
trip_analyze(trip_mtr, ind_sab, "Sábados")
#barras de tempos de viagem nos domingos
ind_dom = (dt >= 3) & (dt < 4)
trip_analyze(trip_mtr, ind_dom, "Domingos")
#end


##parte 2.5 - analises

s = ""
s += "Quantidade de dados analisados:\t"
s += str(len(data_mtr['t']))
s += str("\nQuantidade de ônibus:\t")
s += str(len(np.unique(data_mtr['co'])))
s += str("\nQuantidade de linhas:\t")
s += str(len(np.unique(data_mtr['cl'])))

s += str("\nVelocidade mediana geral:\t")
s += str(np.median(data_mtr['v']))
s += str("\nVelocidade média geral:\t")
s += str(np.mean(data_mtr['v']))
s += str("\nDesvio padrão da velocidade:\t")
s += str(np.std(data_mtr['v']))
s += str("\nCurtose da velocidade:\t")
s += str(scipy.stats.kurtosis(data_mtr['v']))
s += str("\nSkewness da velocidade:\t")
s += str(scipy.stats.skew(data_mtr['v']))

s += str("\nTempo mediano de viagem:\t")
s += str(np.median(trip_mtr['tmp']))
s += str("\nTempo médio de viagem:\t")
s += str(np.mean(trip_mtr['tmp']))
s += str("\nDesvio padrão do tempo de viagem:\t")
s += str(np.std(trip_mtr['tmp']))
s += str("\nCurtose do tempo de viagem:\t")
s += str(scipy.stats.kurtosis(trip_mtr['tmp']))
s += str("\nSkewness do tempo de viagem:\t")
s += str(scipy.stats.skew(trip_mtr['tmp']))

with open("dat.txt", 'w') as datf:
	datf.write(s)

del s
del trip_mtr

#Parte 3 - Distribuição de ônibus ativos
print("parte 3")
#barras de ônibus ativos geral
active_analyze(data_mtr, inds_all, "Geral")
#barras de ônibus ativos em dias úteis
active_analyze(data_mtr, inds_util, "Dias úteis")
#barras de ônibus ativos em sábados
active_analyze(data_mtr, inds_sab, "Sábados")
#barras de ônibus ativos em domingos
active_analyze(data_mtr, inds_dom, "Domingos")
#barras de ônibus ativos nos finais de semana
active_analyze(data_mtr, inds_fds, "Finais de semana")



#Parte 4 - Comparação ida x volta#
print("parte 4")
#init
data_mtr = filter_data(data_mtr, inds_util)
trip_mtr = calc_triptime(data_mtr)
#declaracoes iniciais
t = data_mtr['t']
d = t / (60 * 60 * 24) % 7

ti = trip_mtr['tis']
trip_lin = trip_mtr['lin']
cl = data_mtr['cl']
h = (t % 24)
#indices
inds_all = (t == t)
inds_util = ((d < 2) | (d > 4))
inds_sab = ((d >= 2) & (d < 3))
inds_fds = (d >= 2) & (d < 4)
inds_ida = (cl < 15000)
inds_volta = (cl > 15000)
#ida

inds_trip_ida = (trip_lin < 15000)
suptitle = "Ida - dias úteis"
trip_analyze(trip_mtr, inds_trip_ida, suptitle)
vel_analyze(data_mtr, inds_ida, suptitle)
active_analyze(data_mtr, inds_ida, suptitle)

#volta
inds_trip_volta = (trip_lin > 15000)
suptitle = "Volta - dias úteis"
trip_analyze(trip_mtr, inds_trip_volta, suptitle)
vel_analyze(data_mtr, inds_volta, suptitle)
active_analyze(data_mtr, inds_volta, suptitle)

#outros
dif_bar_analyze(data_mtr, inds_ida, inds_volta,
	"Diferença ida x volta - dias úteis")

#end
del trip_lin
del trip_mtr
del ti

#Parte 5 - Comparação espacial de horários de picos
print("parte 5")
matrix_size = 75
dif_size = 3

#util
interval_analyze(data_mtr, inds_util,
	"Dias úteis", matrix_size)

#matinal todos
manha_inds = (h > 7.5) & (h < 8.5)
interval_analyze(data_mtr, manha_inds,
	"Dias úteis - pico matinal", matrix_size)

#manhã ida
manha_ida_inds = manha_inds & (cl < 15000)
interval_analyze(data_mtr, manha_ida_inds,
	"Dias úteis - pico matinal- linhas de ida", matrix_size)

#matinal volta
manha_volta_inds = manha_inds & (cl > 15000)
interval_analyze(data_mtr, manha_volta_inds,
	"Dias úteis - pico matinal - linhas de volta", matrix_size)

#tarde todos
tarde_inds = (h > 17.5) & (h < 18.5) & inds_util
interval_analyze(data_mtr, tarde_inds,
	"Dias úteis - pico vespertino", matrix_size)

#tarde ida
tarde_ida_inds = tarde_inds & (cl < 15000)
interval_analyze(data_mtr, tarde_ida_inds,
	"Dias úteis - pico vespertino - linhas de ida", matrix_size)

#tarde volta
tarde_volta_inds = tarde_inds & (cl > 15000)
interval_analyze(data_mtr, tarde_volta_inds,
	"Dias úteis - pico vespertino - linhas de volta", matrix_size)

#diferença matinal
dif_analyze(data_mtr,
	manha_ida_inds, manha_volta_inds,
	matrix_size, dif_size, "Dias úteis - pico matinal - diferença ida x volta")
#diferença vespertino
dif_analyze(data_mtr,
	tarde_ida_inds, tarde_volta_inds,
	matrix_size, dif_size, "Dias úteis - pico vespertino - diferença ida x volta")
#diferenca manha vs tarde
dif_analyze(data_mtr,
	manha_ida_inds, tarde_ida_inds,
	matrix_size, dif_size, "Dias úteis - diferença manhã x tarde - ida")
dif_analyze(data_mtr,
	manha_volta_inds, tarde_volta_inds,
	matrix_size, dif_size, "Dias úteis - diferença manhã x tarde - volta")
#diferenca de periodo
dif_analyze(data_mtr,
	manha_inds, tarde_inds,
	matrix_size, dif_size, "Dias úteis - diferença manhã x tarde")
################15
matrix_size = 15
#diferença matinal
dif_analyze(data_mtr,
	manha_ida_inds, manha_volta_inds,
	matrix_size, dif_size, "Dias úteis - pico matinal - diferença ida x volta")
#diferença vespertino
dif_analyze(data_mtr,
	tarde_ida_inds, tarde_volta_inds,
	matrix_size, dif_size, "Dias úteis - pico vespertino - diferença ida x volta")
#diferenca manha vs tarde
dif_analyze(data_mtr,
	manha_ida_inds, tarde_ida_inds,
	matrix_size, dif_size, "Dias úteis - diferença manhã x tarde - ida")
dif_analyze(data_mtr,
	manha_volta_inds, tarde_volta_inds,
	matrix_size, dif_size, "Dias úteis - diferença manhã x tarde - volta")
#diferenca de periodo
dif_analyze(data_mtr,
	manha_inds, tarde_inds,
	matrix_size, dif_size, "Dias úteis - diferença manhã x tarde")

#Parte 6 - Análise de zonas
print("parte 6")
#75
matrix_size = 75
#zona oeste
y_i = -23.52
y_e = -23.62
x_i = -46.67
x_e = -46.77
matrix_cfg = {'x_i': x_i, 'x_e': x_e, 'y_i': y_i, 'y_e': y_e, 'c': matrix_size}
zone_analyze(data_mtr, matrix_cfg, "Zona oeste")
#zona leste
y_i = -23.45
y_e = -23.70
x_i = -46.35
x_e = -46.60
matrix_cfg = {'x_i': x_i, 'x_e': x_e, 'y_i': y_i, 'y_e': y_e, 'c': matrix_size}
zone_analyze(data_mtr, matrix_cfg, "Zona leste")
#centro
y_i = -23.50
y_e = -23.60
x_i = -46.60
x_e = -46.70
matrix_cfg = {'x_i': x_i, 'x_e': x_e, 'y_i': y_i, 'y_e': y_e, 'c': matrix_size}
zone_analyze(data_mtr, matrix_cfg, "Centro")
#extremo sul
y_i = -23.62
y_e = -23.92
x_i = -46.60
x_e = -46.80
matrix_cfg = {'x_i': x_i, 'x_e': x_e, 'y_i': y_i, 'y_e': y_e, 'c': matrix_size}
zone_analyze(data_mtr, matrix_cfg, "Extremo sul")


#15
matrix_size = 15
#zona oeste
y_i = -23.52
y_e = -23.62
x_i = -46.67
x_e = -46.77
matrix_cfg = {'x_i': x_i, 'x_e': x_e, 'y_i': y_i, 'y_e': y_e, 'c': matrix_size}
zone_analyze(data_mtr, matrix_cfg, "Zona oeste")
#zona leste
y_i = -23.45
y_e = -23.70
x_i = -46.35
x_e = -46.60
matrix_cfg = {'x_i': x_i, 'x_e': x_e, 'y_i': y_i, 'y_e': y_e, 'c': matrix_size}
zone_analyze(data_mtr, matrix_cfg, "Zona leste")
#centro
y_i = -23.50
y_e = -23.60
x_i = -46.60
x_e = -46.70
matrix_cfg = {'x_i': x_i, 'x_e': x_e, 'y_i': y_i, 'y_e': y_e, 'c': matrix_size}
zone_analyze(data_mtr, matrix_cfg, "Centro")
#extremo sul
y_i = -23.62
y_e = -23.92
x_i = -46.60
x_e = -46.80
matrix_cfg = {'x_i': x_i, 'x_e': x_e, 'y_i': y_i, 'y_e': y_e, 'c': matrix_size}
zone_analyze(data_mtr, matrix_cfg, "Extremo sul")
"""Parte 7 - misc"""

