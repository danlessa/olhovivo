# -*- coding: iso-8859-15 -*-
#################### Dependências #########################
import numpy as np
import matplotlib.pyplot as plt;
import matplotlib.pylab as pylab;
import os;
import struct;
import time;
import csv;
import math;
#################### Variáveis globais #########################
dat_filename="posicoes.dat";
DPI=300;
grad_to_x=100;
grad_to_y=100;
hr=60*60;
UTC=-2*hr;
fgn=0;
mtr_map_size=200;
ang_map_size=30;
current_folder="";

#################### Rotinas de cálculos #########################

### salvar figura ###
#fignum: numero da figura, dpip:resolucao em DPI a usar, inch=array 2x1 do tamanho da figura
def savefig(fignum, dpip, inch=[12,9]):
	fig=plt.gcf();
	fig.set_size_inches(inch[0],inch[1]);
	plt.savefig(current_folder+"fig"+str(fignum)+".png",dpi=dpip,format='png');
	plt.close();

### separar em dia de semana ###
def day_separate(td,day):
	##1970/1/1 -> thursday	
	td_days=np.mod(td,24*hr*7);
	inds=(td_days%7==(day+3));
	return inds;	

### calcula distancia em km entre dois pontos esféricos ###
def dist_coord(lat1, long1, lat2, long2):
    degrees_to_radians = math.pi/180.0;
    phi1 = (90.0 - lat1)*degrees_to_radians;
    phi2 = (90.0 - lat2)*degrees_to_radians;
    theta1 = long1*degrees_to_radians;
    theta2 = long2*degrees_to_radians;
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2));
    arc = math.acos( cos );
    return 6371*arc;

#### pega tempos e velocidades e retorna velocidades medianas em intervalos de hora, bem como o tempo medio no intervalo, quantidades e desvio-padroes ####
def calc_vel_hora(td,vd):
	t=np.mod(td,hr*24); # transformar tempos em hora do dia
	v=vd;	
	length=len(t);
	interval=0.5*hr; #intervalo das barras
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
	return {'std':stds, 'med':meds, 'tmp':temps, 'qtd':qtds};
	
### calcula direcao instantanea ###
def get_direction(x1,y1,x2,y2):
	dy=y2-y1;
	dx=np.cos(math.pi*y1/180)*(x2-x1);
	return np.arctan2(dy,dx);	

### processar dados ###
def adjust_data(cl,co,px,py,td,vd):
	'''
	length=len(td);
	bus_qtd=len(np.unique(co));	
	angsize=length-bus_qtd;
	xf=np.zeros(angsize,dtype=np.float64);
	yf=np.zeros(angsize,dtype=np.float64);
	tf=np.zeros(angsize,dtype=np.float64);
	vf=np.zeros(angsize,dtype=np.float64);
	cof=np.zeros(angsize,dtype=np.int32);
	ang=np.zeros(angsize,dtype=np.float64);
	clf=np.zeros(angsize,dtype=np.int32);
	count=0;
	w=np.zeros(max(co)+1,dtype=np.int32);
	j=0;
	for i in range(0,length):
		tco=co[i];
		if(w[tco]==0):
			w[tco]=i;
			continue;
		else:
			cl1=cl[w[tco]];
			x1=px[w[tco]];
			y1=py[w[tco]];
			t1=td[w[tco]];			
			v1=vd[w[tco]];
			x2=px[i];
			y2=py[i]
			t2=td[i];
			v2=td[i];
			ang[j]=get_direction(x1,y1,x2,y2);
			xf[j]=(x1+x2)/2;
			yf[j]=(y1+y2)/2;
			tf[j]=(t2+t1)/2;
			vf[j]=(v2+v1)/2;
			cl[j]=cl1;
			cof[j]=tco;
			w[tco]=i;
			j+=1;
		if(i%100000==0):
			print(length-i);

	return {'x':xf, 'y':yf, 'ang':(90*ang/(math.pi)), 't':tf,'co':cof, 'cl':clf, 'v':vf};
	'''
	return {'cl':cl, 'co':co, 'x':px, 'y':py, 'v':vd, 't':td, 'ang':np.zeros(len(td))};

### calcula matriz de angulos nas posicoes ###
def calc_ang_matrix(px,py,angd,c,vd):
	x_init=-46.30;
	x_end=-46.85;
	y_init=-23.37;
	y_end=-23.92;
	
	interval=0.55/(c-1);
	ang_mtr=np.zeros((c,c),dtype=np.float64);
	q_mtr=np.zeros((c,c),dtype=np.int32);
	py_cache=[];
	px_cache=[];
	ang_cache=[];
	v_cache=[];
	for j in range(0,c):
		y_inds=((py>=y_end+interval*j)&(py<y_end+interval*(j+1)));
		py_cache.append(py[y_inds]);
		px_cache.append(px[y_inds]);
		ang_cache.append(angd[y_inds]);
		v_cache.append(vd[y_inds]);
		if(j%10==0):
			print("cache-" + str(c-j));

	for i in range(0,c):		
		for j in range(0, c):
			x_inds=((px_cache[j]>=x_end+interval*i)&(px_cache[j]<x_end+interval*(i+1)));
			if(len(x_inds)<1):
				continue;
			ang_sq=ang_cache[j][x_inds];	
			mcos=np.mean(np.cos(ang_sq)/v_cache[j][x_inds]);
			msin=np.mean(np.sin(ang_sq)/v_cache[j][x_inds]);	
			mang=np.arctan2(msin,mcos);			
			q_mtr[i,j]=len(ang_sq);	
			ang_mtr[i,j]=mang;
		if(i%100==0):
			print(c-i);
	ang_mtr=np.transpose(np.fliplr(ang_mtr));
	q_mtr=np.transpose(np.fliplr(q_mtr));
	return {'ang_mtr':ang_mtr, 'qtd_mtr':q_mtr};

### calcula matriz de velocidades as posicoes ###
def calc_vel_matrix(px,py,vd,c):
	x_init=-46.30;
	x_end=-46.85;
	y_init=-23.37;
	y_end=-23.92;
	
	interval=0.55/(c-1);
	v_mtr=np.zeros((c,c),dtype=np.float64);
	q_mtr=np.zeros((c,c),dtype=np.int32);
	py_cache=[];
	px_cache=[];
	v_cache=[];
	for j in range(0,c):
		y_inds=((py>=y_end+interval*j)&(py<y_end+interval*(j+1)));
		py_cache.append(py[y_inds]);
		px_cache.append(px[y_inds]);
		v_cache.append(vd[y_inds]);
		if(j%10==0):
			print("cache-" + str(c-j));
	for i in range(0,c):		
		for j in range(0, c):
			x_inds=((px_cache[j]>=x_end+interval*i)&(px_cache[j]<x_end+interval*(i+1)));
			if(len(x_inds)<1):
				continue;
			v_sq=v_cache[j][x_inds];		
			q_mtr[i,j]=len(v_sq);	
			v_mtr[i,j]=np.median(v_sq);
		if(i%100==0):
			print(c-i);
	v_mtr=np.transpose(np.fliplr(v_mtr));
	q_mtr=np.transpose(np.fliplr(q_mtr));
	return {'v_mtr':v_mtr, 'qtd_mtr':q_mtr};

### calcula tempo de viagens ###
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
	tis=[];

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
				tis.append(m_ti[co_i]);
			m_n[co_i]=n+1;
			m_ti[co_i]=t_i;
			m_cl[co_i]=cl_i;
		m_tl[co_i]=t_i;
		if(i%100000==0):
			print(lengthd-i);
	return {'tmp':times, 'lin':lines, 'tis':tis};		

def calc_active_bus(td, cod):
	
	intervalhr=0.5;
	interval=intervalhr*hr;
	bcount=int(24/intervalhr);
	tmid=np.zeros(bcount,0);
	buscount=np.zeros(bcount,0);
	modtd=np.mod(td,bcount);
	for i in range(0, bcount):
		inds=(modtd>=i*interval) & (motd<(i+1)*interval);
		buscount[i]=np.unique(cod[inds]);
		tmid[i]=(i*interval + (i+1)*interval)/2;	
	return {'active_bus':buscount, 'tmid':tmid};


### calcula tempo de saidas ###
def exit_times(lines, tis):
	print("NI");

#################### Rotinas de mapas matriciais #########################

### mapa de matriz ###
def map_mtr(mtr,fignum, title):
	fig=plt.figure(fignum);
	ax=fig.add_subplot(111);
	plt.title(title);
	ax.set_axis_bgcolor('black');
	cax=ax.matshow(mtr,cmap='nipy_spectral');
	fig.colorbar(cax);
	savefig(fignum,DPI);

### mapa de velocidades medianas ##
def map_vel(v_mtr,fignum):
	map_mtr(v_mtr,fignum,"Velocidade mediana (km/h)");

def map_ang(a_mtr,fignum):
	map_mtr(a_mtr,fignum,"Direção (graus)");

### mapa de direções ###
def map_dir(d_mtr,fignum):
	map_mtr(d_mtr,fignum,"Direções (rad)");

### mapa de densidade de ônibus ###
def map_qtd(q_mtr,fignum):
	map_mtr(q_mtr,fignum,"Distribuição normalizada dos ônibus");

#################### Rotinas de plots/dispersão #########################

### grafico de dispersao colorida das velocidades ###
def plot_vel_pos(pxd,pyd,vdd,fignum):

	px=pxd;
	py=pyd;
	vd=vdd;
	color=vd;
	vdmedian=np.median(vd);
	
	fig=plt.figure(fignum);
	ax=fig.add_subplot(111);
	ax.set_axis_bgcolor('black');
	plt.xlabel("Latitude (º)");
	plt.ylabel("Longitude (º)");
	plt.title("Velocidade do ônibus");
	plt.scatter(px,py,c=color,marker='.',alpha=1,linewidth=0,cmap='nipy_spectral');
	plt.colorbar();
	savefig(fignum,DPI,[20,15]);

### velocidade x hora ###
def plot_vel_t(vd,td,fignum):

	t=np.mod(td,hr*24);
	plt.figure(fignum);
	plt.xlabel("Hora do dia(h)");
	plt.ylabel("Velocidade (km/h)");
	plt.title("Velocidade x tempo");
	plt.xticks(np.arange(0, 24, 4));
	plt.plot(t/hr,vd,'.',markersize=0.01);
	savefig(fignum,DPI);

### tempo de viagem x hora ###
def plot_tem_t(times, tis,fignum):
	t=np.array(tis);	
	t=np.mod(t,hr*24);
	timnp=np.array(times);
	inds=((timnp<300)&(timnp>0));
	plt.figure(fignum);
	plt.xlabel("Hora do dia(h)");
	plt.xticks(np.arange(0, 24, 4));
	plt.ylabel("Tempo de viagem (min)");
	plt.title("Tempo de viagem x hora");
	plt.plot(t[inds]/hr,timnp[inds],'.',markersize=0.1);
	savefig(fignum,DPI);

#################### Rotinas de histogramas #########################

### rotina generica para histograma ###
def histogram(dat, xlabel, ylabel, title, bins, figurenum):
	bc=bins;
	plt.figure(figurenum);
	plt.ylabel(ylabel);
	plt.xlabel(xlabel);
	plt.title(title);
	plt.hist(dat, bins=bc);
	savefig(figurenum,DPI);

### histograma de tempos de viagem ###
def hist_triptime(times,fignum):
	t=np.array(times);
	histogram(t[(t<300)&(t>0)],"Tempo de viagem (min)","Viagens","Tempos de viagens",50,fignum);

### histograma de velocidades medianas ###
def hist_vel(vd,fignum):
	histogram(vd,"Velocidade (km/h)","Quantidade de elementos de velocidade","Histograma de velocidades",140,fignum);

### histograma de velocidades de linhas ###
def rank_linha(vd,cld,fignum):
	v=vd;
	cl=np.unique(cld);
	qtd=len(cl);
	vms=np.zeros(qtd,dtype=np.float64);
	for i in range(0,qtd):
		inds=(cld == cl[i]);
		vms[i]=np.median(v[inds]);
	bc=150;
	plt.figure(fignum);
	plt.ylabel("Quantidade de elementos de velocidades medianas na linha");
	plt.xlabel("Velocidade mediana (km/h)");
	plt.title("Histograma de velocidades x linhas");
	plt.hist(vms, bins=bc);
	savefig(fignum,DPI);

#################### Rotinas de barras #########################

### onibus ativos por hora -- corigir ###
def bar_activebus_t(cod,td,figurenum):
	t=np.mod(td,hr*24);
	v=cod;	
	length=len(t);
	interval=0.5*hr;
	bar_c=24*int(hr/interval);

	temps=np.zeros(bar_c,dtype=np.float64);
	qtds=np.zeros(bar_c,dtype=np.int32);
	for i in range(0, bar_c):
		inds = ((t>=i*interval) & (t<(i+1)*interval));
		temps[i]=(i*interval+(i+1)*interval)/2;
		qtds[i]=len(v[inds]);
	width=0.3;
	plt.figure(figurenum);
	plt.title("Quantidade de ônibus ativos por hora");
	plt.xlabel("Hora do dia");
	plt.ylabel("Onibus ativos");
	plt.xticks(np.arange(0, 24, 4));
	plt.bar(temps/hr,qtds,width);
	savefig(figurenum,DPI);

### quantidade de dados por hora ###
def bar_point_t(td,figurenum):
	t=np.mod(td,hr*24);
	length=len(t);
	interval=0.5*hr;
	bar_c=24*int(hr/interval);

	temps=np.zeros(bar_c,dtype=np.float64);
	qtds=np.zeros(bar_c,dtype=np.int32);
	for i in range(0, bar_c):
		inds = ((t>=i*interval) & (t<(i+1)*interval));
		temps[i]=(i*interval+(i+1)*interval)/2;
		qtds[i]=len(t[inds]);	
	width=0.3;
	plt.figure(figurenum);
	plt.title("Quantidade de dados por hora");
	plt.xlabel("Hora do dia");
	plt.ylabel("Dados");
	plt.xticks(np.arange(0, 24, 4));
	plt.bar(temps/hr,qtds,width);
	savefig(figurenum,DPI);
	
### barras de tempos de viagem por hora ###
def bar_triptime_t(times,tis,fignum1,fignum2):
	width=0.35;
	tnp=np.array(times);
	tisnp=np.array(tis);
	inds=((tnp<300)&(tnp>0));
	tisnp=tisnp[inds];
	tnp=tnp[inds];	
	t=np.mod(tisnp,hr*24);
	length=len(t);
	interval=0.5*hr;
	bar_c=24*int(hr/interval);

	stds=np.zeros(bar_c,dtype=np.float64);
	meds=np.zeros(bar_c,dtype=np.float64);	
	temps=np.zeros(bar_c,dtype=np.float64);
	qtds=np.zeros(bar_c,dtype=np.int32);
	for i in range(0, bar_c):
		inds = ((t>=i*interval) & (t<(i+1)*interval));
		meds[i]=np.median(tnp[inds]);
		if np.isnan(meds[i]):
			meds[i]=0;
		stds[i]=np.std(tnp[inds]);
		if np.isnan(stds[i]):
			stds[i]=0;
		temps[i]=(i*interval+(i+1)*interval)/2;
		qtds[i]=len(tnp[inds]);
	
	width=0.3;
	plt.figure(fignum1);
	plt.title("Tempo mediano de viagem por hora do dia");
	plt.xlabel("Hora do dia");
	plt.ylabel("Tempo (min)");
	plt.xticks(np.arange(0, 24, 2));
	plt.yticks(np.arange(0,60,3));
	plt.grid(True);
	plt.bar(temps/hr,meds,width);	
	savefig(fignum1,DPI);
	
	plt.figure(fignum2);
	plt.title("Desvio padrão dos tempos de viagem por hora do dia");
	plt.xlabel("Hora do dia");
	plt.ylabel("Desvio padrão (min)");	
	plt.xticks(np.arange(0,24,2));
	plt.yticks(np.arange(0,15,1));
	plt.grid(True);
	plt.bar(temps/hr,stds,width);
	savefig(fignum2,DPI);

### barras de velocidades medianas por hora ###
def bar_vel_t(tmp,meds,stds,fignum1,fignum2):
	width=0.3;
	plt.figure(fignum1);
	plt.title("Velocidade mediana por hora do dia");
	plt.xlabel("Hora do dia");
	plt.ylabel("Velocidade mediana (km/h)");
	plt.xticks(np.arange(0, 24, 2));
	plt.yticks(np.arange(0,60,3));
	plt.grid(True);
	plt.bar(tmp/hr,meds,width);
	savefig(fignum1,DPI);

	plt.figure(fignum2);
	plt.title("Desvio padrão das velocidades por hora do dia");
	plt.xlabel("Hora do dia");
	plt.ylabel("Desvio padrão (km/h)");	
	plt.xticks(np.arange(0,24,2));
	plt.yticks(np.arange(0,15,1));
	plt.grid(True);
	plt.bar(tmp/hr,stds,width);
	savefig(fignum2,DPI);

#################### Rotinas de carregamento de dados #########################

### carregar e retornar arquivo de codigo de linhas ###
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

### carregar dados ###
def load_dat(filename):
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

	inds=((v<65) & (v>0));
	c_l=c_l[inds];
	c_o=c_o[inds];
	lon=lon[inds];
	lat=lat[inds];
	t=t[inds]+hr*UTC;
	v=v[inds];
	return {'cl':c_l, 'co':c_o, 'lo':lon, 'la':lat, 't':t, 'v':v}

#################### Rotinas de mandar rodar #########################

### rotinas a serem processadas em intervalos especificos ###
def proc_fil(px,py,td,vd,cl,co,ang,iv_t,iv_vm,iv_st,iv_qt,tpt_tmp,tpt_lin,tpt_tis):
	global fgn;
	
	print("Calculando histogramas");
	hist_triptime(tpt_tmp,fgn);
	#rank_linha(vd,cl,fgn+1);
	hist_vel(vd,fgn+2);
	
	print("Calculando matriz de velocidades");
	out3=calc_vel_matrix(px,py,vd,mtr_map_size);

	print("Calculando mapas e  dispersões");
	map_vel(out3['v_mtr'],fgn+3);
	map_qtd(out3['qtd_mtr'],fgn+4);	
	#plot_vel_pos(px,py,vd,fgn+5);
	
	
	print("Calculando ângulos");
	#out41=calc_ang_matrix(px,py,ang,ang_map_size,vd);
	#map_ang(out41['ang_mtr'],fgn+6);
	#fgn+=7;

### rotinas a serem processadas sem intervalos especificos (exceto se for por dias)###
def proc_gen(px,py,td,vd,cl,co,ang,iv_t,iv_vm,iv_st,iv_qt,tpt_tmp,tpt_lin,tpt_tis):
	global fgn;
	print("Calculando barras");	
	bar_vel_t(iv_t,iv_st,iv_vm,fgn,fgn+1);
	bar_activebus_t(co,td,fgn+2);
	bar_point_t(td,fgn+3);
	bar_triptime_t(tpt_tmp,tpt_tis,fgn+4,fgn+5);
	print("Calculando dispersões");
	plot_vel_t(vd,td,fgn+6);
	plot_tem_t(tpt_tmp,tpt_tis,fgn+7);
	fgn+=8;

def proc(px,py,td,vd,cl,co,angs,inds):
	global fgn;
	t_px=px[inds];
	t_py=py[inds];
	t_td=td[inds];
	t_vd=vd[inds];
	t_cl=cl[inds];
	t_co=co[inds];
	t_ang=angs[inds];
	print("Calculando velocidades x hora");
	out1=calc_vel_hora(t_td,t_vd);
	print("Calculando tempos de viagem");
	out2=calc_triptime(t_cl,t_co,t_td);

	#dados calculados de calc_vel_hora
	iv_t=out1['tmp'];
	iv_vm=out1['med'];
	iv_st=out1['std'];
	iv_qt=out1['qtd'];
	
	#dados calculados de calc_triptime
	tpt_tmp=out2['tmp'];
	tpt_lin=out2['lin'];
	tpt_tis=out2['tis'];
	return [t_px, t_py, t_td, t_vd, t_cl, t_co, t_ang, iv_t, iv_vm, iv_st, iv_qt, tpt_tmp, tpt_lin, tpt_tis]

### rotina geral ###
def main():
	global fgn;
	global current_folder;
	fgn=0;
	filename=dat_filename;
	print("Carregando dados");
	out=load_dat(filename);

	#dados originais	
	px=out['lo'];
	py=out['la'];
	td=out['t'];
	vd=out['v'];
	cl=out['cl'];
	co=out['co'];

	print("Processando dados");
	#dados ajustados
	out_aj=adjust_data(cl,co,px,py,td,vd);
	px=out_aj['x'];
	py=out_aj['y'];
	vd=out_aj['v'];
	td=out_aj['t'];
	ang=out_aj['ang'];
	cl=out_aj['cl'];
	co=out_aj['co'];

	del out;	

	#processar analises gerais	
	inds_all = (td == td);
	args=proc(px,py,td,vd,cl,co,ang,inds_all);
	fgn=0*20;
	current_folder="plots/geral/";
	proc_gen(*args);
	proc_fil(*args);


	#processar analises especificas temporais

	#filtro de dia/hora	
	hrt=np.mod(td,hr*24)/hr; #horas
	drt=np.mod(td,7*hr*24)/(24*hr); #dias de semana

	inds_dd=((drt%7<2) | (drt%7>4)); #indice de dia de semana
	inds_df=((drt%7>2) & (drt%7<4)); #indice de final de semana
	inds_m=(hrt>7) & (hrt<9) & inds_dd; #indice de pico matinal
	inds_v=(hrt>17)&(hrt<19) & inds_dd; #indice de pico vespertino
	
	inds_ida=(cl<15000);
	inds_volta=(cl>15000);
	
	
	#analisar picos matinais
	print("Calculando picos matinais");
	fgn=20*1;	
	current_folder="plots/matinal/";
	args=proc(px,py,td,vd,cl,co,ang,inds_m);
	proc_fil(*args);

	#analisar picos vespertinos
	print("Calculando picos vespertinos");
	fgn=20*2;	
	current_folder="plots/vespertino/";
	args=proc(px,py,td,vd,cl,co,ang,inds_v);
	proc_fil(*args);

	#analisar final de semana
	print("Calculando finais de semana");
	fgn=20*3;	
	current_folder="plots/fds/";
	args=proc(px,py,td,vd,cl,co,ang,inds_df);
	proc_gen(*args);
	proc_fil(*args);	
	
	print("Calculando dias úteis");
	fgn=20*4;
	current_folder="plots/util/";
	args=proc(px,py,td,vd,cl,co,ang,inds_dd);
	proc_gen(*args);
	proc_fil(*args);

	#analisar ida - matinal
	print("Calculando ida - matinal");
	fgn=20*5;	
	current_folder="plots/matinal-ida/";
	args=proc(px,py,td,vd,cl,co,ang,inds_m&inds_ida);
	proc_fil(*args);

	#analisar ida - vespertino
	print("Calculando ida - vespertino");
	fgn=20*6;	
	current_folder="plots/vespertino-ida/";
	args=proc(px,py,td,vd,cl,co,ang,inds_v&inds_ida);
	proc_fil(*args);

	#analisar volta - matinal
	print("Calculando volta - vespertino");
	fgn=20*7;	
	current_folder="plots/matinal-volta/";
	args=proc(px,py,td,vd,cl,co,ang,inds_m&inds_volta);
	proc_fil(*args);

	#analisar volta - vespertino
	print("Calculando volta - vespertino");
	fgn=20*8;	
	current_folder="plots/vespertino-volta/";
	args=proc(px,py,td,vd,cl,co,ang,inds_v&inds_volta);
	proc_fil(*args);
	
	#analisar ida/volta
	print("Calculando ida/volta");
	fgn=20*9;	
	current_folder="plots/ida/";
	args=proc(px,py,td,vd,cl,co,ang,inds_ida);
	proc_gen(*args);
	proc_fil(*args);	

	fgn=20*10;	
	current_folder="plots/volta/";
	args=proc(px,py,td,vd,cl,co,ang,inds_volta);
	proc_gen(*args);
	proc_fil(*args);	
	print("Pronto!");	
	fgn=0;
#################### Misc #########################

### init ###
if __name__ == "__main__":
	main();
	
