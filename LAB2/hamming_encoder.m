function saida = hamming_encoder(x)
G = [1 1 0 1;
     1 0 1 1;
     1 0 0 0;
     0 1 1 1;
     0 1 0 0;
     0 0 1 0;
     0 0 0 1;];
 
saida = G*x';
saida = mod(saida', 2);

%saida = zeros(7,1);
%saida(3) = x(1);
%saida(5) = x(2);
%saida(6) = x(3);
%saida(7) = x(4);
%saida(1) = mod(saida(1) + saida(3) + saida(5) + saida(7),2);
%saida(2) = mod(saida(2) + saida(3) + saida(6) + saida(7), 2);
%saida(4) = mod(saida(4) + saida(5) + saida(6) + saida(7), 2);
end