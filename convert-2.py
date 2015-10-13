import struct;
import csv;
import time;
import sys;

dic_bus = {}

with open("posicoes.dat","br") as f_pos:
    with open("posicoes-new.dat", "ab") as f_new:
        while (1==1):
            byt=f_pos.read(32);
            bin=struct.unpack('iiddd',byt);
            code=int(bin[0]);
            p=int(bin[1]);
            px=float(bin[2]);
            py=float(bin[3]);
            t=float(bin[4]);
            
            if(p not in dic_bus):
                dic_bus[p]=[None]*5;
                dic_bus[p][0]=code;
                dic_bus[p][1]=p;
                dic_bus[p][2]=px;
                dic_bus[p][3]=py;
                dic_bus[p][4]=t;
            if(px == dic_bus[p][2] and py == dic_bus[p][3]):
                continue;
            else:
                f_new.write(struct.pack('iiddd',int(dic_bus[p][0]), int(p), float(dic_bus[p][2]), float(dic_bus[p][3]), float(dic_bus[p][4])));
                dic_bus[p][0]=code;
                dic_bus[p][1]=p;
                dic_bus[p][2]=px;
                dic_bus[p][3]=py;
                dic_bus[p][4]=t;
                