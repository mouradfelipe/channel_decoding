import numpy as np
import statistics
import copy
import matplotlib.pyplot as plt
import time
from scipy.stats import norm
import math

from encoder import generate_random_array
from encoder import octal_to_bin
from encoder import encoding
from encoder import encoder
from encoder import transmit_message
from encoder import decoder as decoder1
from encoder import decode as decode1
from encoder_2 import decoder as decoder2
from encoder_2 import decode as decode2

q = 0.5
size = 10000
m = [6]
g1 = [117]
g2 = [127]
g3 = [155]

ratio = [0.31622776601683794, 0.4216965034285822, 0.5623413251903491, 0.7498942093324559, 1.0, 1.333521432163324, 1.7782794100389228, 2.371373705661655, 3.1622776601683795, 4.216965034285822, 5.623413251903491, 7.498942093324558, 10.0]
R_conv = 1/3
p_conv = [None] * len(ratio)
for i in range(0, len(ratio)):
    p_conv[i] = norm.sf(math.sqrt(2*R_conv*ratio[i]))
p_values = p_conv
p_reduced = p_values
#p_values = [5e-1, 3e-1, 1e-1, 8e-2, 6e-2, 4e-2, 2e-2, 9e-3, 7e-3]
#p_reduced = [5e-1, 3e-1, 1e-1, 8e-2, 6e-2, 4e-2, 2e-2, 9e-3, 7e-3]
total = 20
total_reduced = 20

total = total_reduced
p_values = p_reduced

time_bit_encoding_distance = [None] * len(m)
for i in range(0, len(m)):
    time_bit_encoding_distance[i] = [None] * len(p_values)
    for j in range(0, len(p_values)):
        time_bit_encoding_distance[i][j] = [None] * total

avg_time_bit_encoding_distance = [None] * len(m)
std_time_bit_encoding_distance = [None] * len(m)

time_bit_decoding_distance = [None] * len(m)
for i in range(0, len(m)):
    time_bit_decoding_distance[i] = [None] * len(p_values)
    for j in range(0, len(p_values)):
        time_bit_decoding_distance[i][j] = [None] * total

avg_time_bit_decoding_distance = [None] * len(m)
std_time_bit_decoding_distance = [None] * len(m)


error_distance = [None] * len(m)
for i in range(0, len(m)):
    error_distance[i] = [None] * len(p_values)
    for j in range(0, len(p_values)):
        error_distance[i][j] = [None] * total

avg_error_distance = [None] * len(m)
for i in range(0, len(m)):
    avg_error_distance[i] = [None] * len(p_values)

std_error_distance = [None] * len(m)
for i in range(0, len(m)):
    std_error_distance[i] = [None] * len(p_values)

error_prob = [None] * len(m)
for i in range(0, len(m)):
    error_prob[i] = [None] * len(p_values)
    for j in range(0, len(p_values)):
        error_prob[i][j] = [None] * total

avg_error_prob = [None] * len(m)
for i in range(0, len(m)):
    avg_error_prob[i] = [None] * len(p_values)

std_error_prob = [None] * len(m)
for i in range(0, len(m)):
    std_error_prob[i] = [None] * len(p_values)
'''
for k in range(0, len(m)):
    for i, p in enumerate(p_values):
        for j in range(0, total):
            u = generate_random_array(size, q)  # input
            s = time.time()
            [saida, table] = encoder(m[k], g1[k], g2[k], g3[k], u)
            e = time.time()
            time_bit_encoding_distance[k][i][j] = (e-s)/size  # encoding time per bit
            transmitted_message = transmit_message(copy.deepcopy(saida), p)  # receives AWGN
            estados_distance = [-1] * (2 ** m[k])
            estados_distance[0] = [0, 0, []]
            s = time.time()
            error_distance[k][i][j] = (
                np.sum(np.absolute(np.array(u) - np.array(decoder1(transmitted_message, table, estados_distance)))))
            error_distance[k][i][j] /= size  # Pe_hamming_distance(p)
            e = time.time()
            time_bit_decoding_distance[k][i][j] = (e-s)/size  # decoding time per bit
            estados_prob = [-1] * (2 ** m[k])
            estados_prob[0] = [1, 0, []]
            error_prob[k][i][j] = (
                np.sum(np.absolute(np.array(u) - np.array(decoder2(transmitted_message, table, estados_prob, p)))))
            error_prob[k][i][j] /= size  # Pe_prob(p)
        avg_error_distance[k][i] = sum(error_distance[k][i]) / total
        std_error_distance[k][i] = statistics.stdev(error_distance[k][i])
        avg_error_prob[k][i] = sum(error_prob[k][i]) / total
        std_error_prob[k][i] = statistics.stdev(error_prob[k][i])
    avg_time_bit_encoding_distance[k] = np.average(time_bit_encoding_distance[k])
    avg_time_bit_decoding_distance[k] = np.average(time_bit_decoding_distance[k])
    std_time_bit_encoding_distance[k] = np.std(time_bit_encoding_distance[k])
    std_time_bit_decoding_distance[k] = np.std(time_bit_decoding_distance[k])

print("tempo médio de encoding: ", avg_time_bit_encoding_distance, " +- ", std_time_bit_encoding_distance)
print("tempo médio de decoding: ", avg_time_bit_decoding_distance, " +- ", std_time_bit_decoding_distance)

print(avg_error_distance)
print(std_error_distance)
print(avg_error_prob)
print(std_error_prob)
'''


total = 20

avg_error_distance = [[0.48970499999999995, 0.47595, 0.44871, 0.413195, 0.28093, 0.13420500000000002, 0.03812, 0.008405, 0.0008449999999999999, 0.00014, 0.0, 0.0, 0.0]]

std_error_distance = [[0.011397990358415216, 0.01859214604979324, 0.05402171980348567, 0.06348061846778615, 0.07609772871636494, 0.09767071680423274, 0.027075014700875633, 0.012328122536021367, 0.0014405682358379498, 0.0005807436249281923, 0.0, 0.0, 0.0]]

avg_error_prob = [[0.49034500000000003, 0.47615999999999997, 0.44971500000000003, 0.414015, 0.28081, 0.13444000000000003, 0.040894999999999994, 0.008735, 0.0009, 0.00014, 0.0, 0.0, 0.0]]

std_error_prob = [[0.009845676315279876, 0.017674078551131844, 0.052518871545579236, 0.06320013553449824, 0.07629643642088611, 0.09742328912102022, 0.03051307700676962, 0.013116252473453247, 0.0014400292394692255, 0.0005807436249281923, 0.0, 0.0, 0.0]]


xaxis = np.array(p_values)
# Colocar aqui o euclidiano para plotar os 3 juntos para m = 6
avg_error_euclid = [0.481305, 0.45458999999999994, 0.39813, 0.277695, 0.12884, 0.026740000000000003, 0.0019250000000000003, 8.999999999999999e-05, 0.0, 0.0, 0.0, 0.0, 0.0]
std_error_euclid = [0.015179080176347977, 0.03911775683752841, 0.07571359257095123, 0.08627834302419118, 0.061712708577731375, 0.026579191108835498, 0.002938685930820101, 0.00023216373532487797, 0.0, 0.0, 0.0, 0.0, 0.0]


# primeiros 3 plots: comparação m a m de dist x prob
for k in range(len(m)):
    fig = plt.figure(k)
    ax = plt.axes()
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.errorbar(xaxis, np.array(avg_error_distance[k]), yerr=np.array(std_error_distance[k]), fmt='-o')
    ax.errorbar(xaxis, np.array(avg_error_prob[k]), yerr=np.array(std_error_prob[k]), fmt='-o')
    ax.errorbar(xaxis, np.array(avg_error_euclid), yerr=np.array(std_error_euclid), fmt='-o')
    plt.grid()
    plt.title('m = ' + str(m[k]) + ', comparação das variações do algoritmo de Viterbi')
    plt.legend(['Distância de Hamming', 'Probabilidade de ocorrência', 'Distância Euclidiana'], loc='upper right')
    ax.set_xlim(101 / 100 * p_values[0], 100 / 101 * p_values[-3])
    ax.set_ylim(1e-5, 1e-0)
    plt.xlabel('p')
    plt.ylabel('Pe')

# últimos 2 plots: comparação interna (diferença entre m's) dist e prob
fig = plt.figure(len(m))
ax = plt.axes()
ax.set_xscale("log")
ax.set_yscale("log")
legend = []
for k in range(len(m)):
    ax.errorbar(xaxis, np.array(avg_error_distance[k]), yerr=np.array(std_error_distance[k]), fmt='-o')
    legend.append('m = ' + str(m[k]))
plt.grid()
plt.title('Probabilidade de erro utilizando como critério a distância de Hamming')
plt.legend(legend, loc='upper right')
ax.set_xlim(101 / 100 * p_values[0], 100 / 101 * p_values[-1])
ax.set_ylim(1e-5, 1e-0)
plt.xlabel('p')
plt.ylabel('Pe')

# agora o último plot ... prob
fig = plt.figure(len(m) + 1)
ax = plt.axes()
ax.set_xscale("log")
ax.set_yscale("log")
legend = []
for k in range(len(m)):
    ax.errorbar(xaxis, np.array(avg_error_prob[k]), yerr=np.array(std_error_prob[k]), fmt='-o')
    legend.append('m = ' + str(m[k]))
plt.grid()
plt.title('Probabilidade de erro utilizando como critério a probabilidade de ocorrência')
plt.legend(legend, loc='upper right')
ax.set_xlim(101 / 100 * p_values[0], 100 / 101 * p_values[-1])
ax.set_ylim(1e-5, 1e-0)
plt.xlabel('p')
plt.ylabel('Pe')

plt.show()
