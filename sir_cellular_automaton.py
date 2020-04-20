from cellular_automaton import createAC, vicinityVonNeumann, countElem
from numpy import arange, matrix
from numpy.random import uniform
from pylab import plot, show, legend, grid, xlabel, ylabel, xticks, yticks, axvline, axhline, title

# 6 linhas e 5 colunas
m = 6
n = 5

# AC 5x6 inicializado com 0
network = createAC(0, 0, m=m, n=n)

# o indivíduo do meio está infectado
network.itemset((int(m/2), int(n/2)), 1)

# taxas
tau = 0.2

# período infeccioso
k = 5

timeStart = 0
timeStop = 30
timeStep = 1

# tempo
time = arange(timeStart, timeStop, timeStep)

# individuos em t
S = I = R = 0
# populações
pop_S = []
pop_I = []
pop_R = []

# todos os estados da rede em cada t
system = []

for t in time:
    S = countElem(network, 0)
    I = sum([countElem(network, p+1) for p in range(k)])
    R = countElem(network, -1)

    pop_S.append(S)
    pop_I.append(I)
    pop_R.append(R)

    system.append(network.copy())

    print(f't:{t}')
    print(network)
    print('=-='*10)

    for i in range(m):
        for j in range(n):
            cell = (i, j)
            cellState = network.item(cell)
            cellStatePrevious = system[-1].item(cell)
            cellVicinity = vicinityVonNeumann(m=m, n=n, elem=cell)

            N = (cellVicinity['N'], network.item(cellVicinity['N']))
            W = (cellVicinity['W'], network.item(cellVicinity['W']))
            E = (cellVicinity['E'], network.item(cellVicinity['E']))
            S = (cellVicinity['S'], network.item(cellVicinity['S']))

            # regra nº 1: transitar de S -> I
            if 1 <= cellState <= k:
                p_SI_N = uniform()
                p_SI_W = uniform()
                p_SI_E = uniform()
                p_SI_S = uniform()

                if p_SI_N <= tau/3 and N[1] == 0:
                    network.itemset(N[0], 1)
                if p_SI_S <= tau/3 and S[1] == 0:
                    network.itemset(S[0], 1)

                if tau/3 < p_SI_W <= tau and W[1] == 0:
                    network.itemset(W[0], 1)
                if tau/3 < p_SI_E <= tau and E[1] == 0:
                    network.itemset(E[0], 1)

                # período infeccioso
                if cellState < k and cellStatePrevious != 0 and cellStatePrevious != -1:
                    network.itemset(cell, cellState+1)

            # regra nº 2: transitar de I -> R
            if cellState == k:
                network.itemset(cell, -1)

xticks(arange(timeStart, timeStop, 2))
yticks(arange(0, m*n, 2))
axvline(color='grey')
axhline(color='grey')

title('Propagação de uma Infeção numa Sala de Aula\n' +
      rf'm:{m}, n:{n}, L: {m*n}' + '\n' + rf'$k: {k}$ dias, $\tau : 0.2$')
plot(time, pop_S, color='darkorange',
     linestyle='solid', marker='.', label='Sucep.')
plot(time, pop_I, color='brown', linestyle='solid', marker='s', label='Infec.')
plot(time, pop_R, color='purple', linestyle='solid', marker='x', label='Recup.')
xlabel(r'dias')
ylabel(r'Populações')
legend(loc='best')
grid(True)
show()
