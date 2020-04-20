from numpy import arange
import pylab as plb
from tests.tester import test, TODAY, SCHEDULE
from random import randint, uniform
from cellular_automaton import createAC, vicinityVonNeumann, countElem


L = int(input('Network Dimension: '))

P = -0.2        # round(rd.uniform(-0.5, 0.5), 3)
gamma = 0.05    # round(rd.uniform(0, 1), 3)

alpha = round(((1 - gamma)/2) - P, 2)
beta = round(((1 - gamma)/2) + P, 2)

startTime = int(input('Start Time: '))
stopTime = int(input('Stop Time: '))
stepTime = float(input('Step Time: '))
spaceTime = arange(startTime, stopTime+stepTime, stepTime)

network = createAC(0, 2, L=L)

pop_prey = []
pop_predators = []

dirName = test()

for t in spaceTime:
    for v in range(0, L**2):
        i = randint(0, L-1)
        j = randint(0, L-1)
        site = (i, j)
        stateSite = network.item(site)

        vicinity = vicinityVonNeumann(L=L, i=i, j=j)

        vicinity = [
            network.item(vicinity["N"]),
            network.item(vicinity["E"]),
            network.item(vicinity["S"]),
            network.item(vicinity["W"])
        ]

        k = round(uniform(0., 1.), 5)
        if stateSite == 0:
            n = countElem(vicinity, 0)
            if k <= (n*alpha)/4 and n > 0:
                network.itemset(site, 1)
        elif stateSite == 1:
            n = countElem(vicinity, 1)
            if k <= (n*beta)/4 and n > 0:
                network.itemset(site, 2)
        elif stateSite == 2:
            if k <= gamma:
                network.itemset(site, 0)

    pop_prey.append((countElem(network, 1))/(L**2))
    pop_predators.append((countElem(network, 2))/(L**2))
    print(t)

plb.title(
    rf'$L={L}; \alpha={alpha}; \beta={beta}; P={P}; \gamma={gamma}$'
)
plb.plot(spaceTime, pop_prey, '>c', label='presa'); plb.xlabel(r'$t$')
plb.plot(spaceTime, pop_predators, '.r', label='predador'); plb.ylabel(r'$presa, predador$')
plb.legend(); plb.grid()
plb.savefig(f'{dirName}/{TODAY} {SCHEDULE}.png', format='png'); plb.show()
plb.close()

