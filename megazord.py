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
megazord(data_mtr)