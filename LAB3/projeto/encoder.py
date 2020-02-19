import numpy as np
import copy
import time


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
            saida.append(np.dot(g, np.array(list(str(i) + np.binary_repr(estado, width=m)[:]), dtype=int)) % 2)
        table[i][estado] = [proxestado, saida].copy()

    return [saida, proxestado, table]


delta2 = 0


def encoder(m, g1, g2, g3, u):
    g1 = octal_to_bin(g1)
    g2 = octal_to_bin(g2)
    g3 = octal_to_bin(g3)
    table = [[-1] * (2 ** m), [-1] * (2 ** m)]
    saida = []
    estado = 0
    s = time.time()
    for i in np.nditer(u):  # for each entry bit generates output
        [output, estado, table] = encoding(i, [g1, g2, g3], estado, table, m)
        saida.append(output)
    e = time.time()
    global delta2
    delta2+=(e-s)
    # print(table)
    return [saida, table]


delta1 = 0


def decode(estados, saida_i, table, step):
    estados_new = estados.copy()
    for i, estado in enumerate(estados):
        if estado != -1:
            next_estado_0 = table[0][i][0]  # primeiro fazemos pra possivel entrada == 0
            custo_0 = 0
            for j, v in enumerate(saida_i):
                if v == table[0][i][1][j]:
                    pass
                else:
                    custo_0 += 1
            '''
            if estados_new[next_estado_0] == -1:  # primeira vez que o estado é alcançado
                estados_new[next_estado_0] = [estado[0] + custo_0, step, estado[2] + [0]]
            elif estados_new[next_estado_0][1] == step - 1:  # primeira vez do loop que o estado é alcançado
                estados_new[next_estado_0] = [estado[0] + custo_0, step, estado[2] + [0]]
            elif estados_new[next_estado_0][0] > estado[0] + custo_0:  # novo caminho encontrado é
                # melhor do que o último definido
                estados_new[next_estado_0] = [estado[0] + custo_0, step, estado[2] + [0]]
            '''
            if estados_new[next_estado_0] == -1 or estados_new[next_estado_0][1] == step - 1 or \
                    estados_new[next_estado_0][0] > estado[0] + custo_0:
                estados_new[next_estado_0] = [estado[0] + custo_0, step, estado[2] + [0]]
            next_estado_1 = table[1][i][0]  # agora para possivel entrada == 1
            custo_1 = 0
            for j, v in enumerate(saida_i):
                if v == table[1][i][1][j]:
                    pass
                else:
                    custo_1 += 1
            '''
            if estados_new[next_estado_1] == -1:  # primeira vez que o estado é alcançado
                estados_new[next_estado_1] = [estado[0] + custo_1, step, estado[2] + [1]]
            elif estados_new[next_estado_1][1] == step - 1:  # primeira vez do loop que o estado é alcançado
                estados_new[next_estado_1] = [estado[0] + custo_1, step, estado[2] + [1]]
            elif estados_new[next_estado_1][0] > estado[0] + custo_1:  # novo caminho encontrado é
                # melhor do que o último definido
                estados_new[next_estado_1] = [estado[0] + custo_1, step, estado[2] + [1]]
            '''
            if estados_new[next_estado_1] == -1 or estados_new[next_estado_1][1] == step - 1 or \
                    estados_new[next_estado_1][0] > estado[0] + custo_1:
                estados_new[next_estado_1] = [estado[0] + custo_1, step, estado[2] + [1]]

    return estados_new


def decoder(saida, table, estados):
    step = 1
    global delta1
    s = time.time()
    for saida_i in saida:
        estados = decode(estados, saida_i, table, step)
        step += 1
    e = time.time()
    delta1 += (e - s)
    custo = 99999999
    estado_final = 0
    for i, estado in enumerate(estados):
        if estado[0] < custo:
            custo = estado[0]
            estado_final = i
    return estados[estado_final][2]


def transmit_message(msg, p):
    # print('entrada do transmissor: ', msg)
    output = copy.deepcopy(msg)
    noise = (np.random.choice([0, 1], size=3 * len(output), p=[1 - p, p]))
    for i in range(0, len(output)):
        for j in range(0, 3):
            output[i][j] = (msg[i][j] + noise[3 * i + j]) % 2
    # print('saida do transmissor: ', output)
    # print('entrada do transmissor: ', msg)
    return output


if __name__ == "__main__":
    q = 0.5
    size = 10000
    u = generate_random_array(size, q)  # generates random array for input wth 0's and 1's
    # print(u)

    m = 3
    g1 = 13
    g2 = 15
    g3 = 17

    [saida, table] = encoder(m, g1, g2, g3, u)
    print('saida: ', saida)

    # agora vou inserir o erro na saida
    p = 0.20
    transmitted_message = transmit_message(copy.deepcopy(saida), p)

    print('saida do transmissor fora da funcao: ', transmitted_message)
    print('saida original: ', saida)

    estados = [-1] * (2 ** m)
    estados[0] = [0, 0, []]
    caminho = decoder(transmitted_message, table, estados)
    diff = np.absolute(np.array(u) - np.array(caminho))
    erro = (np.sum(diff))
    print(diff)
    print(erro)
    print(1000 * delta1 / size, " ms")
    print(1000000 * delta2 / size, " us")

    # para gerar os graficos, vou usar 20 pontos e fazer media +- desvio padrao para cada valor de p, e cada conjunto de G.
    # Depois preciso implementar o tempo com alguma funcao de calcular tempo.
