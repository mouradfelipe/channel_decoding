clear all
close all
clc


% probabilidade de erro no canal
%p_vec = [];
%for z = 0:4
%    for p = [0.5 0.2 0.1]/10^z
%        p_vec = [p_vec p];
%    end
%end
p_vec = [0.28141455281419936 0.2520003553485626 0.22016538577757427 0.18644582579234087 0.15174183201242103 0.11736532659211585 0.08500335742750553 0.056531882437034005 0.03363735132805715 0.017297824096473114 0.007341122566128312 0.0024176164667380853 0.0005690477923374636];


%[n, pos de g no polyc, d_min]
possible_g = [12 14 15 17 18; 3 1 1 1 1; 4 3 4 5 4];
%possible_g = [17; 1; 5];



%dimensao maxima:
kmax = floor(possible_g(1,end)*4/7);
dim_max = possible_g(1,end) - kmax + 1;

g = zeros(size(possible_g,2),dim_max);

P_B_cycle(1,:) = zeros(1,14);
%18 pois tem 18 probabilidades a serem testadas


tam_aprox = 10^5; % quantidade total de bits transmitidos, aprocximadamente
%% codificacao ciclica:
for i = 1:size(possible_g,2)
    %aqui geramos os g's:
    n = possible_g(1,i);
    k = floor(n*4/7);
    local_gs = cyclpoly(n,k,'all');
    gi = local_gs(possible_g(2,i),:);
    g(i,1:length(gi))=gi;

    %agora, gerar os sinais u:
    qtde_v = floor(tam_aprox/k); %qtde de mensagens emitidas / recebidas. 
    tam = qtde_v*k; %tamanho total da mensagem emitida, aproximadamente tam_aprox, 
    %mas corrigido para nao ter 'meia-mensagens'

    data = mod(floor(rand(qtde_v,k)*10),2); %mensagem a ser emitida

    
    %agora, irei codificar u com v = ug, em seguida transmitir v (colocando
    %o erro) e decodificar v, tentando corrigi-lo. Por fim, comparo
    %o v decodificado com o v correto para ver o indice de acertos de
    %correcao.
    
    v = zeros(qtde_v, n); %v's transmitidos (sem erro)
    data_r = zeros(qtde_v, k); %sera todos os u's recebidos (depois de decoficar o v recebido)


    counter = 1;

    %aqui gero as sindromes fundamentais para este g, para depois poder
    %fazer a decodificacao
    grau_gi = n-k;
    d_min = possible_g(3,i);
    sindromes_gi = sindrom_gen(n, grau_gi, gi, d_min);
    
    for p = p_vec
        for index = 1:qtde_v
            v(index, :) = conv(data(index, :),gi); %aqui encontramos o v
            v = mod(v,2);
            %para um dado u
            received = bsc(v(index, :),  p); %v com erro
            data_r(index, :) = cycle_decoder(received, sindromes_gi, gi); %corrige o v com erro (r), transforma em u, e devolvo em data_r 
        end
        P_B_cycle(i,counter) = sum(sum(abs(data_r - data)))/tam;
        counter = counter+1;
    end
    

end

%% codificacao de Hamming (para comparar no plot):
% tam_aprox = 10^5; % quantidade total de bits transmitidos, aprocximadamente
% 
% k = 4;
% n = 7;
% qtde_v = floor(tam_aprox/k);
% tam = qtde_v*k;
% 
% data = mod(floor(rand(qtde_v,k)*10),2);
% 
% v = zeros(qtde_v, n);
% data_r = zeros(qtde_v, k);
% P_B_hamming = zeros(1, 14);
% 
% 
% counter = 1;
% 
% for p = p_vec
%     for i = 1:qtde_v
%         v(i, :) = hamming_encoder(data(i, :));
%         received = bsc(v(i, :),  p);
%         data_r(i, :) = hamming_decoder(received);
%     end
%     
%     P_B_hamming(counter) = double(sum(sum(abs(data_r - data))))/tam;
%     counter = counter+1;
% end


%% Plot
% 
% epsilon = 10^-5
% 
% for i = 1:size(P_B_cycle,1)
%     for j = 1:size(P_B_cycle,2)
%         if(P_B_cycle(i,j) == 0)
%             P_B_cycle(i,j) = epsilon
%         end
%     end
% end
% for i = 1:length(P_B_hamming)
%     if(P_B_hamming(i) == 0)
%         P_B_hamming(i) = epsilon
%     end
% end
% 
% 
% 
% figure 
% loglog(p_vec, abs(P_B_cycle)'); hold on;
% loglog(p_vec, abs(P_B_hamming)'); hold on;
% loglog(p_vec, p_vec, 'k--');
% legend('n = 12', 'n = 14', 'n = 15', 'n = 17', 'n = 18', 'Hamming', 'nao corrigido');
% xlabel('p');
% ylabel('P_b');
% title('Resultado das codificações');
% set(gca, 'xdir', 'reverse')
