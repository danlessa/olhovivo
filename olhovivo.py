# -*- coding: iso-8859-15 -*-

import datetime;
import time;
import csv;
import requests;
import json;
import struct;
import math;
import os;

def verify(req):
    if(req.status_code==200):
        return json.loads(req.content.decode("utf8-"));
    else:
        return None;

def autenticar(token):
    payload = {"token":token};
    return requests.post("http://api.olhovivo.sptrans.com.br/v0/Login/Autenticar", params=payload);

def returnPosicao(cod, aut):
    payload = {"codigoLinha":cod};
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Posicao", params=payload, cookies=aut.cookies);
    return verify(r);

def buscarLinhas(text, aut):
    payload = {"termosBusca":text};
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Linha/Buscar", params=payload, cookies=aut.cookies);
    return verify(r);
    
def carregarDetalhes(cod, aut):    
    payload = {"codigoLinha":cod};
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Linha/CarregarDetalhes", params=payload, cookies=aut.cookies);
    return verify(r);
    
def buscarParadas(text, aut):
    payload = {"termosBusca":text};
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Parada/Buscar", params=payload, cookies=aut.cookies);
    return verify(r);  
    
def buscarParadasLinha(cod, aut):
    payload = {"codigoLinha":cod};
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Parada/BuscarParadasPorLinha", params=payload, cookies=aut.cookies);
    return verify(r);    
    
def buscarParadasCorredor(cod, aut):
    payload = {"codigoCorredor":cod};
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Parada/BuscarParadasPorCorredor", params=payload, cookies=aut.cookies);
    return verify(r); 
    
def buscarCorredor(aut):
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Corredor", cookies=aut.cookies);
    return verify(r);
    
def previsaoChegada_linha(cod_linha, aut):
    payload = {"codigoLinha":cod_linha};
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Previsao", params=payload, cookies=aut.cookies);
    return verify(r);       
    
def previsaoChegada_parada(cod_parada, aut):
    payload = {"codigoParada":cod_parada};
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Previsao", params=payload, cookies=aut.cookies);
    return verify(r);   
    
def previsaoChegada(cod_parada, cod_linha, aut):
    payload = {"codigoParada":cod_parada,"codigoLinha":cod_linha};
    r = requests.get("http://api.olhovivo.sptrans.com.br/v0/Previsao", params=payload, cookies=aut.cookies);
    return verify(r);   
    
    
def scriptObterCodigos(arquivo, tripfile, aut):
    
    linhas = [];
    
    with open(tripfile) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader);
        for row in spamreader:
            if(row[4] != "1"):
                linhas.append(row[0].strip('\"'));
                
                
    t1=time.time();            
    with open(arquivo, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",");
        for line in linhas:
            bl=buscarLinhas(line,aut);
            for hehe in bl:
                csvwriter.writerow([line, hehe["CodigoLinha"], hehe["Sentido"], hehe["Circular"]]);
    t2=time.time();           
    print("time: " + str(t2-t1));
    print("iter: " + str(len(linhas)));
    
    
def scriptCarregarCodigos(arquivo):
    lines=[];
    with open(arquivo) as csvfile:
        csvreader = csv.reader(csvfile,delimiter=',', quotechar='|');
        for line in csvreader:
            lines.append(line);
    return lines;
    
    
def setDictBus(dictbus,i, code, p, px, py, t, cz, v):
    dictbus[i][0]=code;
    dictbus[i][1]=p;
    dictbus[i][2]=px;
    dictbus[i][3]=py;
    dictbus[i][4]=t;
    dictbus[i][5]=cz;
    dictbus[i][6]=v;
 
 
""" http://www.johndcook.com/blog/python_longitude_latitude/ """ 
def dist_coord(lat1, long1, lat2, long2):
 
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.  (km)
    return 6371*arc
    
def scriptDumpPos(arquivo, linhas, tok, dic_bus):
    aut=autenticar(tok);
    for line in linhas:
        code=line[1];
        jt=returnPosicao(code,aut);
        t2=time.time();
        
        if(type(jt) is not dict):
            aut=autenticar(tok);
            print("zzz");
            continue;
        if(len(jt) != 2):
            continue;
            
        vs=jt["vs"];
        for bus in vs:
            p=bus["p"];
            px=bus["px"];
            py=bus["py"];
            
            if(p not in dic_bus):
                dic_bus[p]=[None]*7;
                setDictBus(dic_bus,p,code,p,px,py,t2,0,-1);
            else:
                cz=dic_bus[p][5];
                
                past_code=dic_bus[p][0];
                past_px=dic_bus[p][2];
                past_py=dic_bus[p][3];
                past_t=dic_bus[p][4];
                past_cz=dic_bus[p][5];
                past_v=dic_bus[p][6];
                
                v=0;
                if(px == past_px and py == past_py):
                    if(cz == 1):
                        setDictBus(dic_bus,p,code,p,px,py,t2,1,v);
                        continue;
                    else:
                        cz=1;
                else:
                    v=60*60*dist_coord(py,px,past_py,past_px)/(t2-past_t)
                    cz=0;
                    
                arquivo.write(struct.pack("iidddd",int(past_code), int(p), float(past_px), float(past_py), float(past_t), float(past_v)));
                setDictBus(dic_bus,p,code,p,px,py,t2,cz,v)
                

def main():
    TOKEN = "ab0855f97de16ac2b98e82920f6f07b1539ec2fc666d2b559303011bb057a25a";
    POSICOES = "posicoes.dat";
    COD_LINHAS = "cod_linhas.csv";
    GTFS_FOLDER = "gtfs/";
    dic_bus = {};
	
	
    with open("n.txt","r") as n_fid:
        n_f=int(n_fid.read(1));
    print(n_f);
    
    n=0;
    linhas=scriptCarregarCodigos(COD_LINHAS);
    t1=0;
    t2=0;
    time_start=time.time()

    while 1==1:	
        n=n+1;
        t1=time.time();
        if(t1-time_start>(24*60*60)):
            n_f+=1;
            new_fn="posicoes-" + n_f + ".dat";
            os.rename("posicoes.raps.dat", new_fn);
            with open("n.txt","w") as n_fid:
                n_fid.write(n_f);
            time_start=time.time();			
        else:
            with open(POSICOES,"ab") as fil:
                scriptDumpPos(fil, linhas, TOKEN, dic_bus);
                t2=time.time();
                delta=t2-t1;
                if(delta<60*3):
                    time.sleep(60*3-delta);
    
main();    
