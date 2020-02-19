function sindromes_gi = sindrom_gen(n, grau_gi, gi, d_min)
    
    sindromes_gi = zeros(1,grau_gi);
    gi_swapped = flip(gi);
    num_layers = floor((d_min-1)/2);
    possiveis_dividendos = dec2bin(2^n-1:-1:0)-'0';
    %filtrar nos dividendos os que possuem no maximo num_layers 1's, e que
    %comecem com 1
    counter = 1;
    for i = 1:size(possiveis_dividendos,1)
        if(possiveis_dividendos(i,1) == 1)
            if(sum(possiveis_dividendos(i,:)) <= num_layers)
                possivel_dividendo_invertido = flip(possiveis_dividendos(i,:));
                [~,r] = deconv(possivel_dividendo_invertido,gi_swapped);
                r = mod(r,2);
                r = flip(r);
                %gerar sindrome
                sindromes_gi(counter,1:length(r)) = r;
                counter = counter+1;
            end
        end
    end
end
