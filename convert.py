import struct;
import csv;
import time;

dic_bus = {}

with open("posicoes.csv","r") as f_pos:
    with open("posicoes-new.dat", "ab") as f_new:
        rdr = csv.reader(f_pos, delimiter=',');
        for row in rdr:
            cl=int(row[0];
            p=int(row[1]);
            px=float(row[2]);
            py=float(row[3]);
            hr=row[4];
            date=row[5];
            t_t=time.strptime(hr+" "+date,"%H:%M %Y-%m-%d");
            t=mktime(t_t);
            if(p not in dic_bus):
                dic_bus[p]=[0,0,0,0];
            if(px == dic_bus[p][2] and py == dic_bus[p][3]):
                continue;
            else:
                dic_bus[p][2]=dic_bus[p][0];
                dic_bus[p][3]=dic_bus[p][1];
                dic_bus[p][0]=px;
                dic_bus[p][1]=py;
                f_new.write(struct.pack('iiddd', cl,p,px,py,t));
        dic_bus={};        