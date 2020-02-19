import numpy as np
import random
import matplotlib.pyplot as plt
import csv


def generate_random_array(size, prob):
    return np.random.choice([0, 1], size=size, p=[1 - prob, prob])


def mourad_codify(msg):  # msg deve ter tamanho 8
    G = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1], [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                  [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
                  [0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1], [0, 0, 0, 0, 1, 0, 0,
                                                               0, 1, 1, 0, 1, 1, 1],
                  [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0]],
                 )
    return msg.dot(G) % 2


def transmit_message(msg, p):
    noise = generate_random_array(msg.size, p)
    return (msg + noise) % 2


def mourad_check(msg):  # msg deve ter tamanho 14
    H = np.array([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1], [1, 1, 1, 0, 1, 1],
                  [1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0],
                  [1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 1]])
    return msg.dot(H) % 2


def read_table(filename):
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile)
        table = []
        for row in readCSV:
            table.append(row[0])
    return table


def mourad_decode(msg, table):  # msg deve ter tamanho 14
    error_pattern = mourad_check(msg)
    error_value = 0
    # print(error_pattern)
    # print(msg)
    idx = 0
    for i in error_pattern:
        error_value = error_value + i * (2 ** (5 - idx))
        idx = idx + 1
    # print(error_value)
    correction = table[error_value]
    correction = (list(correction))
    for idx in range(len(correction)):
        correction[idx] = int(correction[idx])
    # print(correction)
    corrected_msg = (msg + correction) % 2
    return corrected_msg[0:8]


p = 0.01
q = 0.5
size = 1000000
info = generate_random_array(size, q)
n_grupos = info.size // 8
i = 0
total_errors = 0
table = read_table('LUT_table.csv')
p_values = [0.27386399330574296, 0.24377270117291477, 0.21137175445879497, 0.17728671040111676, 0.14252470370130638, 0.10850574088977283, 0.07699273024700702, 0.04985607711949172, 0.028647034206930353, 0.014070662688823577, 0.005620679255335825, 0.0017085297568177756, 0.00036161635821509625]


expected_total_errors_ = []
total_errors_ = []
for p in p_values:
    total_errors = 0
    i = 0
    while i < n_grupos:
        msg = info[i * 8:i * 8 + 8]
        coded_message = mourad_codify(msg)
        transmitted_message = transmit_message(coded_message, p)
        decoded_message = mourad_decode(transmitted_message, table)
        total_errors = total_errors + np.sum(~np.equal(msg, decoded_message))
        i = i + 1
    total_errors_.append(total_errors)
    expected_total_errors = (p * size)
    expected_total_errors_.append(expected_total_errors)
    # print(expected_total_errors)
    # print(total_errors)

for i in range(0, len(total_errors_)):
    total_errors_[i] /= size
    expected_total_errors_[i] /= size

print(total_errors_)
print(expected_total_errors_)
