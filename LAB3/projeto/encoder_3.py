import numpy as np
from scipy.stats import norm
import math
import copy


def generate_random_array(size, prob):
    return np.random.choice([0, 1], size=size, p=[1 - prob, prob])


def octal_to_bin(g):
    casas = 0
    g_copy = g
    g_answ = []
    while (g_copy):
        g_copy = int(g_copy / 10)
        casas += 1
    while (casas):
        g_casa = int(g / (10 ** (casas - 1)))
        g = g - g_casa * (10 ** (casas - 1))
        g_casa = np.binary_repr(g_casa, width=3)
        if len(g_answ) == 0:
            g_answ = [int(x) for x in str(int(g_casa))]
        else:
            g_answ = g_answ + list(map(int, list(g_casa)))
        casas -= 1
    g_answ = np.array(g_answ)
    return g_answ


def encoding(i, G, estado, table, m):
    if table[i][estado] != -1:  # memoization table is filled on position
        proxestado = table[i][estado][0]
        saida = table[i][estado][1]
    else:
        proxestado = int(str(i) + (np.binary_repr(estado, width=m)[:-1]), 2)
        saida = []
        for g in G:
            out = (np.dot(g, np.array(list(str(i) + np.binary_repr(estado, width=m)[:]), dtype=int)) % 2)
            if out == 0:
                out = -1
            saida.append(out)
        table[i][estado] = [proxestado, saida].copy()

    return [saida, proxestado, table]


def encoder(m, g1, g2, g3, u):
    g1 = octal_to_bin(g1)
    g2 = octal_to_bin(g2)
    g3 = octal_to_bin(g3)
    table = [[-1] * (2 ** m), [-1] * (2 ** m)]
    saida = []
    estado = 0

    for i in np.nditer(u):  # for each entry bit generates output
        [output, estado, table] = encoding(i, [g1, g2, g3], estado, table, m)
        saida.append(output)
    # print(table)
    return [saida, table]


def decode(estados, saida_i, table, step):
    estados_new = estados.copy()
    for i, estado in enumerate(estados):
        if (estado != -1):
            next_estado_0 = table[0][i][0]  # primeiro fazemos pra possivel entrada == 0
            # custo_0 = np.linalg.norm(np.array(saida_i)-np.array(table[0][i][1]))
            custo_0 = 0
            for j, v in enumerate(saida_i):
                custo_0 += (v - table[0][i][1][j])*(v - table[0][i][1][j])
            custo_0 = math.sqrt(custo_0)
            if estados_new[next_estado_0] == -1:  # primeira vez que o estado é alcançado
                estados_new[next_estado_0] = [estado[0] + custo_0, step, estado[2] + [0]]
            elif estados_new[next_estado_0][1] == step - 1:  # primeira vez do loop que o estado é alcançado
                estados_new[next_estado_0] = [estado[0] + custo_0, step, estado[2] + [0]]
            elif estados_new[next_estado_0][0] > estado[0] + custo_0:  # novo caminho encontrado é
                # melhor do que o último definido
                estados_new[next_estado_0] = [estado[0] + custo_0, step, estado[2] + [0]]

            next_estado_1 = table[1][i][0]  # agora para possivel entrada == 1
            # custo_1 = np.linalg.norm(np.array(saida_i) - np.array(table[1][i][1]))
            custo_1 = 0
            for j, v in enumerate(saida_i):
                custo_1 += (v - table[1][i][1][j]) * (v - table[1][i][1][j])
            custo_1 = math.sqrt(custo_1)
            if estados_new[next_estado_1] == -1:  # primeira vez que o estado é alcançado
                estados_new[next_estado_1] = [estado[0] + custo_1, step, estado[2] + [1]]
            elif estados_new[next_estado_1][1] == step - 1:  # primeira vez do loop que o estado é alcançado
                estados_new[next_estado_1] = [estado[0] + custo_1, step, estado[2] + [1]]
            elif estados_new[next_estado_1][0] > estado[0] + custo_1:  # novo caminho encontrado é
                # melhor do que o último definido
                estados_new[next_estado_1] = [estado[0] + custo_1, step, estado[2] + [1]]
    return estados_new


def decoder(saida, table, estados):
    step = 1
    for saida_i in saida:
        estados = decode(estados, saida_i, table, step)
        step += 1
    custo = 99999999
    estado_final = 0
    for i, estado in enumerate(estados):
        if estado[0] < custo:
            custo = estado[0]
            estado_final = i
    return estados[estado_final][2]


def transmit_message(msg, var):  # var is the variance of the AWGN
    # print('entrada do transmissor: ', msg)
    output = copy.deepcopy(msg)

    # noise = np.random.normal(0, math.sqrt(var), 3 * len(output))
    # print('noise: ', noise, noise[0], noise[1])
    # index = 0
    for i in range(0, len(output)):
        for j in range(0, 3):
            # index2 = (3*i) + j
            output[i][j] = msg[i][j] + list(np.random.normal(0, math.sqrt(var), 1))[0]
            # index += 1
            # print(3*i + j)
    # print('saida do transmissor: ', output)
    # print('entrada do transmissor: ', msg)
    return output


if __name__ == "__main__":
    q = 0.5
    size = 10000

    m = 6
    g1 = 117
    g2 = 127
    g3 = 155

    ratio = [0.31622776601683794, 0.4216965034285822, 0.5623413251903491, 0.7498942093324559, 1.0, 1.333521432163324, 1.7782794100389228, 2.371373705661655, 3.1622776601683795, 4.216965034285822, 5.623413251903491, 7.498942093324558, 10.0]

    R_conv = 1 / 3
    p_conv = [None] * len(ratio)
    for i in range(0, len(ratio)):
        p_conv[i] = norm.sf(math.sqrt(2 * R_conv * ratio[i]))
    total = 20
    error_euclid = [None] * len(ratio)
    for i in range(0, len(ratio)):
        error_euclid[i] = [None] * total

    avg_error_euclid = [None] * len(ratio)
    std_error_euclid = [None] * len(ratio)

    var = [None] * len(ratio)
    for i in range(0, len(ratio)):
        var[i] = 1/(2*ratio[i]*R_conv)

    '''
    R = 1 / 3
    p = 0.14
    rate = (norm.isf(p)) ** 2 / (2 * R)  # Ei/N0
    Eb = 1
    Ei = Eb / R
    N0 = Ei / rate
    var = N0 / 2  # 1/((norm.isf(p)) ** 2)
    '''
    # print(var)
    # print(norm.sf(1/math.sqrt(var)))
    for i, v in enumerate(var):
        for j in range(0, total):
            u = generate_random_array(size, q)  # generates random array for input with 0's and 1's
            # print(u)

            [saida, table] = encoder(m, g1, g2, g3, u)
            # print('saida: ', saida)
            # agora vou inserir o erro na saida
            transmitted_message = transmit_message(copy.deepcopy(saida), v)
            estados = [-1] * (2 ** m)
            estados[0] = [0, 0, []]
            error_euclid[i][j] = (np.sum(np.absolute(np.array(u) - np.array(decoder(transmitted_message, table, estados)))))/size
            print(error_euclid[i][j])
        avg_error_euclid[i] = np.average(error_euclid[i])
        std_error_euclid[i] = np.std(error_euclid[i])
    print(avg_error_euclid)
    print(std_error_euclid)
