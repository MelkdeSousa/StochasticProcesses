from numpy import arange, array, average, matrix, power, sqrt, std
from numpy.random import randint, uniform
from pylab import (errorbar, grid, legend, plot, show, subplot, title, xlabel,
                   xticks, ylabel, yticks)
from ac import countElem, createAC, vicinityVonNeumann

processes = int(input('processes: '))

row = int(input('rows: '))
column = int(input('columns: '))

nI = int(input('I(0): '))

tau = float(input('tau(%): '))/100
delta = float(input('delta(%): '))/100
k = int(input('k: '))

timeStart = 0
timeStop = int(input('t: '))
timeStep = 1

time = arange(timeStart, timeStop, timeStep)

resultsInfec = []
resultsRecov = []

for p in range(processes):
    network = createAC(0, 0, m=row, n=column)

    for v in range(nI):
        x = randint(0, row-1)
        y = randint(0, column-1)

        network.itemset((x, y), 1)

    S = I = R = 0

    pop_S = []
    pop_I = []
    pop_R = []

    for t in time:
        S = countElem(network, 0) / (row*column)
        I = sum([countElem(network, p+1) for p in range(k)]) / (row*column)
        R = countElem(network, -1) / (row*column)

        pop_S.append(S)
        pop_I.append(I)
        pop_R.append(R)

        previousAC: matrix = network.copy()

        for i in range(row):
            for j in range(column):
                cell = (i, j)
                cellVicinity = vicinityVonNeumann(m=row, n=column, elem=cell)
                cellState = network.item(cell)
                cellStatePrevious = previousAC.item(cell)
                
                if uniform() <= delta and 1 <= cellState <= k:
                    cellSwap = (randint(0, row-1), randint(0, column-1))
                    
                    cellSwapState = network.item(cellSwap)
                    cellSwapStatePrevious = previousAC.item(cellSwap)

                    if cellSwap < cell:
                        if cellState < k: cellState += 1
                        else: cellState = -1
                        if cellStatePrevious == 0: cellStatePrevious = 1

                    previousAC.itemset(cell, cellSwapStatePrevious)
                    previousAC.itemset(cellSwap, cellStatePrevious)

                    network.itemset(cell, cellSwapState)
                    network.itemset(cellSwap, cellState)

                    cellState = network.item(cell)
                    cellStatePrevious = previousAC.item(cell)

                N = (cellVicinity['N'], network.item(cellVicinity['N']))
                W = (cellVicinity['W'], network.item(cellVicinity['W']))
                E = (cellVicinity['E'], network.item(cellVicinity['E']))
                S = (cellVicinity['S'], network.item(cellVicinity['S']))

                if 1 <= cellState <= k:
                    if uniform() <= tau/3 and N[1] == 0:
                        network.itemset(N[0], 1)
                    if uniform() <= tau/3 and S[1] == 0:
                        network.itemset(S[0], 1)

                    if uniform() <= tau and W[1] == 0:
                        network.itemset(W[0], 1)
                    if uniform() <= tau and E[1] == 0:
                        network.itemset(E[0], 1)

                    if cellState < k and cellStatePrevious != 0 and cellStatePrevious != -1:
                        network.itemset(cell, cellState+1)

                if cellState == k:
                    network.itemset(cell, -1)

    resultsInfec.append(pop_I)
    resultsRecov.append(pop_R)

averageInfec = []
averageRecov = []

errorSTDInfec = []
errorSTDRecov = []

auxInfec = []
auxRecov = []

for day in time:
    for process in range(processes):
        auxInfec.append(resultsInfec[process][day])
        auxRecov.append(resultsRecov[process][day])

    averageInfec.append(average(auxInfec))
    averageRecov.append(average(auxRecov))

    errorSTDInfec.append(std(auxInfec))
    errorSTDRecov.append(std(auxRecov))

    auxInfec.clear()
    auxRecov.clear()

title('Propagação de uma Infeção com Mobilidade\n' +
      rf'L: {row}x{column}' + '\n' + rf'$k: {k}$ dias, $\tau : {tau*100}\%$, $\delta: {delta*100}\%$, $I(0)={round((nI*100)/(row*column), 2)}\%$')

if processes == 1:
    plot(time, pop_S, label='Pop. Sucep.')
    plot(time, pop_I, label='Pop. Infec.')
    plot(time, pop_R, label='Pop. Recup.')
else:
    errorbar(time, averageInfec, errorSTDInfec, color='darkgreen',
             label=f'Média de Infec | {processes} PEs', marker='.', ms=10, lolims=True, uplims=True,)
    errorbar(time, averageRecov, errorSTDRecov, color='orange',
             label=f'Média de Recup | {processes} PEs', marker='.', ms=10, lolims=True, uplims=True,)

ylabel(r'$\%$ de Infectados e Recuperados')
xlabel(r'dias')
legend(loc='best')

show()
