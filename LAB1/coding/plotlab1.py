import numpy as np
import matplotlib.pyplot as plt

epsilon = .01

input1 = np.array([500491, 197080, 66972, 19560, 3413, 898,
                   231, 30, 9, 5, 0, 0, 0, 0, 0, 0, 0, 0])

xaxis = np.array([5e-1, 2e-1, 1e-1, 5e-2, 2e-2, 1e-2, 5e-3, 2e-3,
                  1e-3, 5e-4, 2e-4, 1e-4, 5e-5, 2e-5, 1e-5, 5e-6, 2e-6, 1e-6])

input2 = np.array([500021, 239034, 92201, 28444, 4912, 1308,
                   315, 49, 18, 6, 0, 0, 0, 0, 0, 0, 0, 0])

input3 = np.array([500000.0, 200000.0, 100000.0, 50000.0, 20000.0, 10000.0,
                   5000.0, 2000.0, 1000.0, 500.0, 200.0, 100.0, 50.0, 20.0, 10.0, 5.0, 2.0, 1.0])


for idx in range(len(input1)):
    if(input1[idx] == 0):
        input1[idx] = epsilon
for idx in range(len(input2)):
    if(input2[idx] == 0):
        input2[idx] = epsilon


# plt.plot(xaxis, input1)
input1 = input1/1000000
input2 = input2/1000000
input3 = input3/1000000
fig, ax = plt.subplots()


ax.loglog(xaxis, input1)
ax.loglog(xaxis, input2)
ax.loglog(xaxis, input3)
ax.grid()
ax.set_xlim(5e-1, 5.1e-4)
ax.set_ylim(1e-6, 1e-0)
plt.legend(['Hamming', 'nosso projeto', 'não codificado'], loc='upper right')
plt.title('Porcentagem de erro obtido versus probabilidade de inversão de bit - zoom')
plt.xlabel('%')
plt.ylabel('%')
plt.show()
