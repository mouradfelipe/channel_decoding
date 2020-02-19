clear all
close all
clc

% n = 10;
% k = 5;
% 
% d(1) = calculate_d_min(n,k);
% 
% 
% n = 12
% k = 6
% 
% d(2) = calculate_d_min(n,k);
% 
% 
% 
% n = 14
% k = 7
% 
% d(3) = calculate_d_min(n,k);
% 
% 
% 
% n = 18
% k = 10
% 
% d(4) = calculate_d_min(n,k);
% 
% 
% 
% n = 20
% k = 10
% 
% d(5) = calculate_d_min(n,k);


for n = 10:20
    k = floor(n*4/7);
    [result_d, result_i] =  calculate_d_min(n,k);
    d(1,n-9) = result_d;
    d(2,n-9) = result_i;
    
end

result = max(d(1,:))



