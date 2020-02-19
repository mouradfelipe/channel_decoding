import numpy as np
from scipy.stats import norm
import math
import matplotlib.pyplot as plt

ratiodB = [-10, -7.5, -5, -2.5, 0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20]

ratio = [None] * len(ratiodB)

for i in range(0, len(ratiodB)):
    ratio[i] = 10**(ratiodB[i]/20)

print(ratio)
# ratio = [0.31622776601683794, 0.4216965034285822, 0.5623413251903491, 0.7498942093324559, 1.0, 1.333521432163324, 1.7782794100389228, 2.371373705661655, 3.1622776601683795, 4.216965034285822, 5.623413251903491, 7.498942093324558, 10.0]
# ratio = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

R_nao_cod = 1
R_conv = 1/3
R_hamming = 4/7
R_ciclico = 9/17
p_nao_cod = [None] * len(ratio)
p_conv = [None] * len(ratio)
p_hamming = [None] * len(ratio)
p_ciclico = [None] * len(ratio)

for i in range(0, len(ratio)):
    p_nao_cod[i] = norm.sf(math.sqrt(2*R_nao_cod*ratio[i]))
    p_conv[i] = norm.sf(math.sqrt(2*R_conv*ratio[i]))
    p_hamming[i] = norm.sf(math.sqrt(2*R_hamming*ratio[i]))
    p_ciclico[i] = norm.sf(math.sqrt(2*R_ciclico*ratio[i]))

print("p_nao_cod: ", p_nao_cod)
print("p_conv: ", p_conv)
print("p_hamming: ", p_hamming)
print("p_ciclico: ", p_ciclico)

# p_nao_cod = [0.2132280183576204, 0.1792140844067709, 0.14445619392505682, 0.11035196001605396, 0.07864960352514251, 0.05122310597474616, 0.02965528762603682, 0.014711024390164388, 0.005953867147778654, 0.0018414175522474582, 0.0003987963351591626, 5.381589265905682e-05, 3.872108215522035e-06]
data_nao_cod = p_nao_cod
data_hamming = [0.29016, 0.25146, 0.21224, 0.1689, 0.11877, 0.07885, 0.04254, 0.01999, 0.00667, 0.00147, 0.00028, 3e-05, 0.0]
data_proprio = [0.327166, 0.293627, 0.253633, 0.20603, 0.155933, 0.10496, 0.060728, 0.028429, 0.010175, 0.002483, 0.000389, 2.4e-05, 2e-06]
data_ciclico = [0.372733727337273, 0.344843448434484, 0.298902989029890, 0.248872488724887, 0.185121851218512, 0.120691206912069, 0.0659206592065921, 0.0236402364023640, 0.00664006640066401, 0.00104001040010400, 7.00007000070001e-05, 0, 0]
data_conv_hamming = [0.48970499999999995, 0.47595, 0.44871, 0.413195, 0.28093, 0.13420500000000002, 0.03812, 0.008405, 0.0008449999999999999, 0.00014, 0.0, 0.0, 0.0]
data_conv_prob = [0.49034500000000003, 0.47615999999999997, 0.44971500000000003, 0.414015, 0.28081, 0.13444000000000003, 0.040894999999999994, 0.008735, 0.0009, 0.00014, 0.0, 0.0, 0.0]
data_conv_euclid = [0.481305, 0.45458999999999994, 0.39813, 0.277695, 0.12884, 0.026740000000000003, 0.0019250000000000003, 8.999999999999999e-05, 0.0, 0.0, 0.0, 0.0, 0.0]


xaxis = np.array(ratiodB)
ax = plt.axes()
plt.plot(xaxis, data_nao_cod)
plt.plot(xaxis, data_hamming)
plt.plot(xaxis, data_proprio)
plt.plot(xaxis, data_ciclico)
plt.plot(xaxis, data_conv_hamming)
plt.plot(xaxis, data_conv_prob)
plt.plot(xaxis, data_conv_euclid)
ax.set_yscale("log")
ax.grid()
ax.set_xlim(ratiodB[0], ratiodB[-1])
ax.set_ylim(1e-6, 1e-0)
plt.legend(['Não codificado', 'Hamming', 'projeto próprio', 'cíclico', 'conv Hamming', 'conv probabilidade', 'conv dist euclidiana'], loc='upper right')
plt.title('Probabilidade de erro obtida versus Ei/N0')
plt.xlabel('Ei/N0 (dB)')
plt.ylabel('Pe')
plt.show()