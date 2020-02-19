import numpy as np
import random
import matplotlib.pyplot as plt


def generate_random_array(size, prob):
    return np.random.choice([0, 1], size=size, p=[1 - prob, prob])


def hamming_codify(msg):  # msg deve ter tamanho 4
    G = np.array([[1, 0, 0, 0, 1, 1, 1], [0, 1, 0, 0, 1, 0, 1],
                  [0, 0, 1, 0, 1, 1, 0], [0, 0, 0, 1, 0, 1, 1]])
    return msg.dot(G) % 2


def transmit_message(msg, p):
    noise = generate_random_array(msg.size, p)
    return (msg + noise) % 2


def hamming_check(msg):  # msg deve ter tamanho 7
    H = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 0], [
        0, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    return msg.dot(H) % 2


def hamming_decode(msg):  # msg deve ter tamanho 7
    error_pattern = hamming_check(msg)
    if np.sum(np.equal(error_pattern, [0, 0, 0])) == 3:
        corrected_msg = msg
    if np.sum(np.equal(error_pattern, [0, 0, 1])) == 3:
        corrected_msg = (msg + [0, 0, 0, 0, 0, 0, 1]) % 2
    if np.sum(np.equal(error_pattern, [0, 1, 0])) == 3:
        corrected_msg = (msg + [0, 0, 0, 0, 0, 1, 0]) % 2
    if np.sum(np.equal(error_pattern, [0, 1, 1])) == 3:
        corrected_msg = (msg + [0, 0, 0, 1, 0, 0, 0]) % 2
    if np.sum(np.equal(error_pattern, [1, 0, 0])) == 3:
        corrected_msg = (msg + [0, 0, 0, 0, 1, 0, 0]) % 2
    if np.sum(np.equal(error_pattern, [1, 0, 1])) == 3:
        corrected_msg = (msg + [0, 1, 0, 0, 0, 0, 0]) % 2
    if np.sum(np.equal(error_pattern, [1, 1, 0])) == 3:
        corrected_msg = (msg + [0, 0, 1, 0, 0, 0, 0]) % 2
    if np.sum(np.equal(error_pattern, [1, 1, 1])) == 3:
        corrected_msg = (msg + [1, 0, 0, 0, 0, 0, 0]) % 2
    return corrected_msg[0:4]


p = 0.01
q = 0.5
size = 100000
info = generate_random_array(size, q)
n_grupos = info.size // 4
i = 0
total_errors = 0
p_values = [0.27386399330574296, 0.24377270117291477, 0.21137175445879497, 0.17728671040111676, 0.14252470370130638, 0.10850574088977283, 0.07699273024700702, 0.04985607711949172, 0.028647034206930353, 0.014070662688823577, 0.005620679255335825, 0.0017085297568177756, 0.00036161635821509625]

expected_total_errors_ = []
total_errors_ = []
for p in p_values:
    total_errors = 0
    i = 0
    while i < n_grupos:
        msg = info[i * 4:i * 4 + 4]
        coded_message = hamming_codify(msg)
        transmitted_message = transmit_message(coded_message, p)
        decoded_message = hamming_decode(transmitted_message)
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