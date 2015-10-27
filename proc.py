#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt
import os;
import struct;
import time;
import csv;

""" http://www.johndcook.com/blog/python_longitude_latitude/ """ 
'''unidade: km'''
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

def calc_triptime(cld, cod, td):
	co=np.unique(cod);
	lengthd=len(td);	

	max_co=np.max(co)+1;
	m_ti=np.zeros(max_co, dtype=np.float64);
	m_tl=np.zeros(max_co, dtype=np.float64);
	m_cl=np.zeros(max_co, dtype=np.int32);
	m_n=np.zeros(max_co, dtype=np.int32);

	times = [];	
	lines = [];

	for i in range(0,lengthd):
		cl_i=cld[i];
		co_i=cod[i];
		t_i=td[i];
		clt=m_cl[co_i];
		n=m_n[co_i];
		if(cl_i != clt):			
			if(n > 1):
				tt=m_tl[co_i]-m_ti[co_i];
				times.append(tt/60);
				lines.append(clt);
			m_n[co_i]=n+1;
			m_ti[co_i]=t_i;
			m_cl[co_i]=cl_i;
		m_tl[co_i]=t_i;
		if(i%100000==0):
			print(lengthd-i);
	return [times, lines];		

def hist_triptime(times):
	ttt=np.array(times[0]);
	plt.figure(5);
	plt.title("Tempo de viagem");
	plt.xlabel("Minutos");
	plt.ylabel("Viagens");
	plt.hist(ttt[((ttt<300) & (ttt>0))],bins=100);

def rank_linha(vd,cld):
	v=vd;
	cl=np.unique(cld);
	qtd=len(cl);
	vms=np.zeros(qtd,dtype=np.float64);
	for i in range(0,qtd):
		inds=(cld == cl[i]);
		vms[i]=np.median(v[inds]);
	bc=150;
	plt.figure(4);
	plt.ylabel("Quantidade de elementos de velocidades medianas na linha");
	plt.xlabel("Velocidade mediana (km/h)");
	plt.title("Histograma de velocidades x linhas");
	plt.hist(vms, bins=bc);
		

def hist_vel(vd):
	bc=140;
	plt.figure(3);
	plt.ylabel("Quantidade de elementos de velocidade");
	plt.xlabel("Velocidade (km/h)");
	plt.title("Histograma de velocidades");
	plt.hist(vd, bins=bc);	

def hist_vel_t(vd,td):
	'''definindo horas em segundos e ajuste de hora por UTC'''
	hr=60*60;
	UTC=(-3)*hr;
	
	t=np.mod(td+UTC,hr*24);
	v=vd;	
	length=len(t);
	interval=0.5*hr;
	bar_c=24*int(hr/interval);

	stds=np.zeros(bar_c,dtype=np.float64);
	meds=np.zeros(bar_c,dtype=np.float64);	
	temps=np.zeros(bar_c,dtype=np.float64);
	qtds=np.zeros(bar_c,dtype=np.int32);
	for i in range(0, bar_c):
		inds = ((t>=i*interval) & (t<(i+1)*interval));
		meds[i]=np.median(v[inds]);
		if np.isnan(meds[i]):
			meds[i]=0;
		stds[i]=np.std(v[inds]);
		if np.isnan(stds[i]):
			stds[i]=0;
		temps[i]=(i*interval+(i+1)*interval)/2;
		qtds[i]=len(v[inds]);
	
	width=0.3; 

	plt.figure(1);
	plt.title("Velocidade mediana por hora do dia");
	plt.xlabel("Hora do dia");
	plt.ylabel("Velocidade mediana (km/h)");
	plt.xticks(np.arange(0, 24, 4));
	plt.yticks(np.arange(0,60,3));
	plt.bar(temps/hr,meds,width);

	plt.figure(2);
	plt.title("Desvio padrão das velocidades por hora do dia");
	plt.xlabel("Hora do dia");
	plt.ylabel("Desvio padrão (km/h)");	
	plt.xticks(np.arange(0,24,2));
	plt.yticks(np.arange(0,15,3));
	plt.bar(temps/hr,stds,width);

	return {'m':meds, 't':temps, 'q':qtds, 's':stds};
''' carregar codigos de linha '''

def load_cod():
	filename="cod_linhas.csv";
	cod_pub = [];
	cod_int = [];
	direction = [];
	circula = [];
	with open(filename,'r') as fid:
		reader=csv.reader(fid,delimiter=',');
		for row in reader:
			cod_pub.append(row[0]);
			cod_int.append(int(row[1]));
			direction.append(int(row[2]));
			circula.append(bool(row[3]));

	return {'cp':cod_pub, 'cl':cod_int, 'di':direction, 'ci':circula};

def load_trip():
	filename="/gtfs/trips.txt";


def load_shapes(shapeid):
	filename="/gtfs/shapes.txt";

''' carregar dados e voltar uma dict com eles '''
def load_dat():
	filename="pos.dat"

	size = os.path.getsize(filename);
	length=int((size - size % 40)/40);
	c_l=np.zeros(length,dtype=np.int32);
	c_o=np.zeros(length,dtype=np.int32);
	lon=np.zeros(length,dtype=np.float64);
	lat=np.zeros(length,dtype=np.float64);
	t=np.zeros(length,dtype=np.float64);
	v=np.zeros(length,dtype=np.float64);
	print(str(length));
	t1=time.time();
	with open(filename,"rb") as fid:
		for i in range(0,length):
			c_l[i], c_o[i], lon[i], lat[i], t[i], v[i] = struct.unpack('iidddd',fid.read(40));
			if i % 100000 == 0:
				print(str(length-i));
	t2=time.time();
	print(str(t2-t1));
	print(str(length));

	inds=((v<70) & (v>0));
	c_l=c_l[inds];
	c_o=c_o[inds];
	lon=lon[inds];
	lat=lat[inds];
	t=t[inds];
	v=v[inds];
	return {'cl':c_l, 'co':c_o, 'lo':lon, 'la':lat, 't':t, 'v':v};

def main():
	print("he");

if __name__ == "__main__":
	main();


out=load_dat();


'''
out1=hist_vel_t(out['v'],out['t']);
print(out1['m']);
print(out1['t']);
print(out1['q']);
print(out1['s']);
hist_vel(out['v']);
rank_linha(out['v'],out['cl']);
'''

'''
print(load_cod());
'''

times=calc_triptime(out['cl'],out['co'],out['t']);
'''hist_triptime(times);'''
plt.show();
