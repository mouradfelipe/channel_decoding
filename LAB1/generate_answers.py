import numpy as np

def mourad_check(msg):  # msg deve ter tamanho 14
    H = np.array([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 0, 1], [1, 1, 1, 0, 1, 1], 
    [1, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0],
    [1,0,0,0,0,0], [0,1,0,0,0,0], [0,0,1,0,0,0], [0,0,0,1,0,0], [0,0,0,0,1,0], [0,0,0,0,0,1]])
    return msg.dot(H) % 2

def next(array):
    n = np.sum(array)
    if n == 0:
        return np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    i = array.size - 1
    j = 0
    while array[i] == 1:
        i = i - 1
        j = j + 1
    if j == n:
        return np.array([1]*(n+1) + [0]*(14 - n - 1))
    if j == 0:
        while array[i] == 0:
            i = i - 1
        new_array = []
        for elem in array:
            new_array.append(elem)
        new_array[i] = 0
        new_array[i+1] = 1
        return np.array(new_array)
    while array[i] == 0:
        i = i - 1
    new_array = []
    for elem in array:
        new_array.append(elem)
    for num in range(j):
        new_array[array.size - 1 - num] = 0
    for num in range(j):
        new_array[i+1+num+1] = 1
    new_array[i] = 0
    new_array[i+1] = 1
    return np.array(new_array)

def convert(vector):
    acum = 0
    i = vector.size - 1
    j = 0
    while i >= 0:
        acum = acum + vector[i]*(2**j)
        i = i - 1
        j = j + 1
    return acum

table = {}
for i in range(64):
    table[i] = np.array([])

a = np.array([0]*14)
filled = 0
while(filled < 64):
    error_pattern = mourad_check(a)
    num = convert(error_pattern)
    if table[num].size == 0:
        table[num] = a
        filled = filled + 1
    a = next(a)

print(table)
with open("LUT_table.txt", "w") as text_file:
    for i in range(64):
        for j in range(len(table[i])):
            text_file.write(str(table[i][j]))
        text_file.write("\n")
