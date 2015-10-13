%% script para gerar um histograma das medianas de velocidade de todos os onibus
%% tn deve ser ajustado de acordo com o inicio das medicoes
%% link para conversor de timestamp unix: http://www.epochconverter.com/

tn = (t-1444186800)/(60*60);
n=48;

mini = min(tn);
maxi = max(tn);

lin=linspace(0,24,n+1);

vm=zeros(n,1);
vs=zeros(n,1);

for i=1:n
    vm(i) = median( v ( tn<lin(i+1) & tn>lin(i) & v>0 & v<70) );
    vs(i) = std(v (tn<lin(i+1) & tn>lin(i) & v>0 & v<70 ) );
end

figure
bar(lin(1:n),vm);
ylabel('Velocidade mediana (km/h)');
xlabel('Hora');

figure
bar(lin(1:n),vs);
ylabel('Desvio padrão');
xlabel('Hora');