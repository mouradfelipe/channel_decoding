function saida = hamming_decoder(r)

    H = [1 0 1 0 1 0 1;
         0 1 1 0 0 1 1;
         0 0 0 1 1 1 1];

    sindrome = mod(H*r', 2);

    bit_errado = sum(sindrome.*[1; 2; 4]);
    %bit_errado = bi2de(sindrome'); % converte a sindrome de binario para decimal

    r_corrigido = r;
    if bit_errado ~= 0
        r_corrigido(bit_errado) = not(r(bit_errado));
    end

    R = [0 0 1 0 0 0 0;
         0 0 0 0 1 0 0;
         0 0 0 0 0 1 0;
         0 0 0 0 0 0 1];

    saida = (R*r_corrigido')';
end