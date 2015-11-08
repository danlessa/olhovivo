# -*- coding: iso-8859-15 -*-
#########################################################
'''
olhovivo-wrap.py: Olho Vivo API wrapper

Author: Danilo Lessa Bernardineli
'''
#########################################################

#################### Dependences #########################
import requests
import json


#################### API Wrapper #########################
def verify(req):
	"""
	Verify auth status code and returns itself or nothing
	Keyword arguments:
		req -- auth request
	"""
	if(req.status_code == 200):
		return json.loads(req.content.decode("utf8-"))
	else:
		return None


def autenticar(token):
	"""
	Authenticates using given token
	Keyword arguments:
		token -- API access token
	"""
	payload = {"token": token}
	return requests.post(
		"http://api.olhovivo.sptrans.com.br/v0/Login/Autenticar",
		params=payload)


def returnPosicao(cod, aut):
	"""
	Return bus position
	Keyword arguments:
		cod -- line internal code
		aut -- auth request
	"""
	payload = {"codigoLinha": cod}
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Posicao",
		params=payload,
		cookies=aut.cookies)
	return verify(r)


def buscarLinhas(text, aut):
	"""
	Search for lines using given text
	Keyword arguments:
		text -- text for searching lines
		aut -- auth request
	"""
	payload = {"termosBusca": text}
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Linha/Buscar",
		params=payload,
		cookies=aut.cookies)
	return verify(r)


def carregarDetalhes(cod, aut):
	"""
	Load info about line
	Keyword arguments:
		cod -- line internal code
		aut -- auth request
	"""
	payload = {"codigoLinha": cod}
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Linha/CarregarDetalhes",
		params=payload,
		cookies=aut.cookies)
	return verify(r)


def buscarParadas(text, aut):
	"""
	Search for bus stops
	Keyword arguments:
		text -- text related to the stop (like the street name)
		aut -- auth request
	"""
	payload = {"termosBusca": text}
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Parada/Buscar",
		params=payload,
		cookies=aut.cookies)
	return verify(r)


def buscarParadasLinha(cod, aut):
	"""
	Search for bus stops given line internal code
	Keyword arguments:
		cod -- line internal code
		auth -- auth request
	"""
	payload = {"codigoLinha": cod}
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Parada/BuscarParadasPorLinha",
		params=payload,
		cookies=aut.cookies)
	return verify(r)


def buscarParadasCorredor(cod, aut):
	"""
	Search for bus stops in the corridors
	Keyword arguments:
		cod -- Corridor code
		aut -- auth request
	"""
	payload = {"codigoCorredor": cod}
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Parada/BuscarParadasPorCorredor",
		params=payload,
		cookies=aut.cookies)
	return verify(r)


def buscarCorredor(aut):
	"""
	Get info about the corridors
	Keyword arguments:
		aut -- auth request
	"""
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Corredor",
		cookies=aut.cookies)
	return verify(r)


def previsaoChegada_linha(cod_linha, aut):
	"""
	Get predictions for  bus arrival
	Keyword arguments:
		cod_linha -- internal line code
		aut -- auth request
	"""
	payload = {"codigoLinha": cod_linha}
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Previsao",
		params=payload,
		cookies=aut.cookies)
	return verify(r)


def previsaoChegada_parada(cod_parada, aut):
	"""
	Get predictions for bus arrival at some bus stop
	Keyword arguments:
		cod_parada -- bus stop id
		aut -- auth request
	"""
	payload = {"codigoParada": cod_parada}
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Previsao",
		params=payload,
		cookies=aut.cookies)
	return verify(r)


def previsaoChegada(cod_parada, cod_linha, aut):
	"""
	Get predictions for bus arrival of some line at certain bus stop
	Keyword arguments:
		cod_parada -- bus stop id
		cod_linha -- internal line code
		aut -- auth request
	"""
	payload = {"codigoParada": cod_parada, "codigoLinha": cod_linha}
	r = requests.get(
		"http://api.olhovivo.sptrans.com.br/v0/Previsao",
		params=payload,
		cookies=aut.cookies)
	return verify(r)