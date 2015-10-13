%% script para carregar os dados
clear

fid=fopen('posicoes.raps.dat','rb');
d=dir('posicoes.raps.dat');
l=fix(d.bytes/40);

tempo=cputime;
cl=zeros(l,1);
p=zeros(l,1);
px=zeros(l,1);
py=zeros(l,1);
t=zeros(l,1);
v=zeros(l,1);

for i=1:l
    cl(i)=fread(fid,1,'int32');
    p(i)=fread(fid,1,'int32');
    px(i)=fread(fid,1,'double');
    py(i)=fread(fid,1,'double');
    t(i)=fread(fid,1,'double');
    v(i)=fread(fid,1,'double');
    if mod(i,1e5)==0
        disp(l-i);
    end
end

e=cputime-tempo
fclose(fid);


val=hist3([py px],[150 150]); imagesc(sqrt(val)), colorbar, axis equal, axis xy
