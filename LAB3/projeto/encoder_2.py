import numpy as np
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
    if table[i][estado] != -1:
        proxestado = table[i][estado][0]
        saida = table[i][estado][1]
    else:
        proxestado = int(str(i) + (np.binary_repr(estado, width=m)[:-1]), 2)
        saida = []
        for g in G:
            saida.append(np.dot(g, np.array(list(str(i) + np.binary_repr(estado, width=m)[:]), dtype=int)) % 2)
        table[i][estado] = [proxestado, saida].copy()

    return [saida, proxestado, table]


def encoder(m, g1, g2, g3, u):
    g1 = octal_to_bin(g1)
    g2 = octal_to_bin(g2)
    g3 = octal_to_bin(g3)
    table = [[-1] * (2 ** m), [-1] * (2 ** m)]
    saida = []
    estado = 0

    for i in np.nditer(u):
        [output, estado, table] = encoding(i, [g1, g2, g3], estado, table, m)
        saida.append(output)
    # print(table)
    return [saida, table]


def decode(estados, saida_i, table, step, p):
    estados_new = estados.copy()
    for i, estado in enumerate(estados):
        if estado != -1:
            next_estado_0 = table[0][i][0]  # primeiro fazemos pra possivel entrada == 0
            # custo_0 = np.sum(np.absolute(np.array(saida_i) - np.array(table[0][i][1])))
            prob_0 = 1  # custo feito com fator p
            for j, v in enumerate(saida_i):
                if v == table[0][i][1][j]:
                    prob_0 *= 1 - p
                else:
                    prob_0 *= p

            if estados_new[next_estado_0] == -1:  # primeira vez que o estado é alcançado
                estados_new[next_estado_0] = [estado[0] * prob_0, step, estado[2] + [0]]
            elif estados_new[next_estado_0][1] == step - 1:  # primeira vez do loop que o estado é alcançado
                estados_new[next_estado_0] = [estado[0] * prob_0, step, estado[2] + [0]]
            elif estados_new[next_estado_0][0] < estado[0] * prob_0:  # novo caminho encontrado é
                # melhor do que o último definido (prob atualmente definida é menor do que a nova).
                estados_new[next_estado_0] = [estado[0] * prob_0, step, estado[2] + [0]]

            next_estado_1 = table[1][i][0]  # agora para possivel entrada == 1
            # custo_1 = np.sum(np.absolute(np.array(saida_i) - np.array(table[1][i][1])))
            prob_1 = 1  # custo feito com fator p
            for j, v in enumerate(saida_i):
                if v == table[1][i][1][j]:
                    prob_1 *= 1 - p
                else:
                    prob_1 *= p

            if estados_new[next_estado_1] == -1:  # primeira vez que o estado é alcançado
                estados_new[next_estado_1] = [estado[0] * prob_1, step, estado[2] + [1]]
            elif estados_new[next_estado_1][1] == step - 1:  # primeira vez do loop que o estado é alcançado
                estados_new[next_estado_1] = [estado[0] * prob_1, step, estado[2] + [1]]
            elif estados_new[next_estado_1][0] < estado[0] * prob_1:  # novo caminho encontrado é
                # melhor do que o último definido (prob atualmente definida é menor do que a nova).
                estados_new[next_estado_1] = [estado[0] * prob_1, step, estado[2] + [1]]
    # renormalização das probabilidades:
    max_prob = 0
    for estado in estados_new:
        if estado != -1:
            if estado[0] > max_prob:
                max_prob = estado[0]
    for estado in estados_new:
        if estado != -1:
            estado[0] /= max_prob
    return estados_new


def decoder(saida, table, estados, p):
    step = 1
    for saida_i in saida:
        estados = decode(estados, saida_i, table, step, p)
        step += 1
    prob = 0
    estado_final = 0
    for i, estado in enumerate(estados):
        if estado[0] > prob:
            prob = estado[0]
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
    u = generate_random_array(size, q)
    # print(u)

    m = 3
    g1 = 13
    g2 = 15
    g3 = 17

    [saida, table] = encoder(m, g1, g2, g3, u)
    print('saida: ', saida)

    # agora vou inserir o erro na saida
    p = 0.1
    transmitted_message = transmit_message(copy.deepcopy(saida), p)

    print('saida do transmissor fora da funcao: ', transmitted_message)
    print('saida original: ', saida)

    estados = [-1] * (2 ** m)
    estados[0] = [1, 0, []]
    caminho = decoder(transmitted_message, table, estados, p)
    diff = np.absolute(np.array(u) - np.array(caminho))
    erro = (np.sum(diff))
    print(diff)
    print(erro)

