function [d,i] = calculate_d_min(n,k)

    pol = cyclpoly(n,k,'all');

    d = 0;
    i = 0;
    if(~isempty(pol))
        for j = 1:size(pol,1)
            g = pol(j,:);
            for i = 0:2^k - 1 
                u = de2bi(i, k);
                v(i+1,:) = mod(conv(u,g),2);
            end

        %achamos todos os v's! Agora, achar as distancias. E descobrir qual a
        %minima. 

             d(j) = n;

             for i = 1:size(v,1)    
                 for c = 1:size(v,1)
                     if(i ~= c)
                         d(j) = min(d(j),sum(xor(v(i,:), v(c,:))));
                     end
                 end
             end

        end
        [d,i] = max(d);
    end

    
end
