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
m = [3, 4, 6]
g1 = [13, 25, 117]
g2 = [15, 33, 127]
g3 = [17, 37, 155]

ratio = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
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

avg_error_distance = [[0.525015, 0.39417500000000005, 0.02954, 0.00698, 0.00235, 0.00031000000000000005, 4e-05, 0.0, 5.5e-05], [0.507745, 0.41698, 0.00736, 0.0036250000000000006, 0.0011699999999999998, 0.00010999999999999999, 5.9999999999999995e-05, 2.9999999999999997e-05, 0.0], [0.49941, 0.4791550000000001, 0.0023150000000000002, 0.00061, 4.4999999999999996e-05, 3.9999999999999996e-05, 0.0, 0.0, 0.0]]

std_error_distance = [[0.048375518765068286, 0.09905035866987852, 0.0363052613267003, 0.01595644070587172, 0.009231325388103956, 0.0009547113093550984, 0.00017888543819998318, 0.0, 0.0002459674775249769], [0.04877476132289387, 0.09315666826430227, 0.01029232723925935, 0.009228780782792606, 0.002355084086106392, 0.0003007009355349247, 0.0002683281572999747, 0.00013416407864998736, 0.0], [0.0074874561768333535, 0.022563395484489344, 0.004162776780745731, 0.00129204040999213, 0.00014680814547887784, 0.00013917047478769187, 0.0, 0.0, 0.0]]

avg_error_prob = [[0.500955, 0.4010000000000001, 0.031830000000000004, 0.005905, 0.0027300000000000002, 0.00045, 0.0, 0.0, 0.0], [0.5018800000000001, 0.41318, 0.006225, 0.00392, 0.0007199999999999999, 0.00010999999999999999, 0.0, 0.0, 0.0], [0.5000449999999999, 0.4791649999999999, 0.0024699999999999995, 0.00073, 3.5e-05, 6.000000000000001e-05, 0.0, 0.0, 0.0]]

std_error_prob = [[0.0051807817942854965, 0.09640285538466062, 0.03868233787089264, 0.013463184694018838, 0.008251194490879231, 0.001112370631153408, 0.0, 0.0, 0.0], [0.00482772693598354, 0.09322641708284869, 0.008904278983192649, 0.01007287133056435, 0.0015793403019848777, 0.0003007009355349247, 0.0, 0.0, 0.0], [0.005514810203347647, 0.021590282292589053, 0.004092882139828401, 0.0015891407807531188, 0.00010894228312566053, 0.00016026294183720633, 0.0, 0.0, 0.0]]
'''

xaxis = np.array(p_values)

# primeiros 3 plots: comparação m a m de dist x prob
for k in range(len(m)):
    fig = plt.figure(k)
    ax = plt.axes()
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.errorbar(xaxis, np.array(avg_error_distance[k]), yerr=np.array(std_error_distance[k]), fmt='-o')
    ax.errorbar(xaxis, np.array(avg_error_prob[k]), yerr=np.array(std_error_prob[k]), fmt='-o')
    #    ax.loglog(xaxis, avg_error_distance[k])
    #    ax.loglog(xaxis, avg_error_prob[k])
    plt.grid()
    plt.title('m = ' + str(m[k]))
    plt.legend(['Distância de Hamming', 'Probabilidade de ocorrência'], loc='upper right')
    ax.set_xlim(101 / 100 * p_values[0], 100 / 101 * p_values[-1])
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
