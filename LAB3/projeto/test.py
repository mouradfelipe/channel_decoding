import time

deltasum = 0
deltamult = 0


sum = 0
mult = 1
for i in range(0, 10000000):
    ssum = time.time()
    sum+=1
    esum =time.time()
    deltasum+=(esum-ssum)
    smult = time.time()
    mult*=1
    emult =time.time()
    deltamult+=(emult-smult)




print("mult: ", deltamult)
print("sum: ", deltasum)