%% criar um histograma contendo a mediana das velocidades por linha
linhas = unique(cl);

N=length(linhas);
vl=zeros(N,1);
sl=zeros(N,1);

for i=1:N
   vl(i) = median( v ( cl == cl(i) & v>0 & v<70));
   sl(i) = std( v ( cl == cl(i) & v>0 & v<70));
   if mod(i,1e2) == 0
       disp([i N-i]);
   end
end

figure
hist(vl,50);
xlabel('Velocidade mediana (km/h)');
ylabel('Quantidade de linhas (ida OU volta)');

figure
hist(sl,50);
xlabel('Desvio padrão das velocidades por linha');
ylabel('Quantidade de linhas (ida OU volta)');