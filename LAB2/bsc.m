function saida = bsc(entrada, p)
    for i = 1:length(entrada)
        if rand > p
            saida(i) = entrada(i);
        else
           saida(i) = not(entrada(i));
        end    
    end
    
end



           
    