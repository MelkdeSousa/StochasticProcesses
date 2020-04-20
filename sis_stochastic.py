import random as rd
import numpy as np
from pylab import plot, legend, grid, show

N = 100  # int(input('Total de pessoas: '))
I = 2

pop_S = []
pop_I = []

beta = 1.0
b = 0.25
gamma = 0.25
h = 0.001

pt = np.arange(0, 100, h)

for t in pt:
    probUP = (beta*I*(N-I)*h / N)
    probDOWN = (b+gamma)*I*h

    k = rd.uniform(0, 1)

    if k <= probUP:
        I += 1
    elif k > probUP and k <= probDOWN + probUP:
        I -= 1
    else:
        I = I

    pop_S.append(N - I)
    pop_I.append(I)

plot(pt, pop_S, label='S(t)')
plot(pt, pop_I, label='I(t)')
legend()
grid()
show()
