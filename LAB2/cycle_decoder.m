function u_decoded = cycle_decoder(received, sindromes_gi, gi)

    
    gi_swapped = flip(gi);
    
    received_invertido = flip(received);
    [q,r] = deconv(received_invertido,gi_swapped);
    r = mod(r,2);
    r = flip(r);
    %r é o resto da divisao da palavra com erro por g. iremos rodar r e a
    %palavra errada received, até encontrar r == alguma sindrome. 
    counter = 0;
    limit = 2^(length(gi)-1);
    while(sum(r) ~= 0 && counter <= limit)
        if(ismember(r,sindromes_gi, 'rows'))
            received(1) = not(received(1));
            received = circshift(received,-counter, 2);
            counter = 0;
            received_invertido = flip(received);
            [q,r] = deconv(received_invertido,gi_swapped);
            r = mod(r,2);
            r = flip(r);
        else
            received = circshift(received,1, 2);
            counter = counter + 1;
            %agora para rodar o resto:
            raux = r(1:length(gi)-1);
            raux = circshift(raux,1,2);
            if(raux(1) == 1)
                raux(1) = 0;
                raux = raux + gi(1:end-1);
                raux = mod(raux,2);
            end
            r(1:length(raux)) = raux;
        end
    end
    u_decoded = flip(mod(q,2));
end
   