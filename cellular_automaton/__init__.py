"""
    ===
    Cellular Automaton
    ===

    Developer:
    ---
        Melk de Sousa

    Project:
    ===
        Processos Estocásticos em Sistemas Biológicos
"""

from numpy import matrix, array, count_nonzero
from random import randint, uniform


def createAC(start, end, **kwargs):
    try:
        try:
            m = kwargs['m']
            n = kwargs['n']
        except KeyError:
            m, n = kwargs['L'], kwargs['L']
    except:
        print('Undeclared Dimension')
        exit(1)

    return matrix([
        [randint(start, end) for j in range(n)]
        for i in range(m)
    ])


def vicinityVonNeumann(**kwargs):
    try:
        if 'show' not in kwargs: show = False
        elif kwargs['show'] == False: show = False
        elif kwargs['show'] == True: show = True

        try:
            m = kwargs['m']
            n = kwargs['n']
        except KeyError:
            m, n = kwargs['L'], kwargs['L']

        try:
            i = kwargs['i']
            j = kwargs['j']
        except:
            i = kwargs['elem'][0]
            j = kwargs['elem'][1]

    except:
        print('Undeclared Dimension')
        exit(1)

    N = ((m+i-1) % m, j)
    W = (i, (n+j-1) % n)
    E = (i, (j+1) % n)
    S = ((i+1) % m, j)

    vicinity = {
        "N": N,
        "W": W,
        "E": E,
        "S": S
    }

    if show:
        for k, v in vicinity.items():
            print(f'{k}: {v}')
    return vicinity


def vicinityMoore(**kwargs):
    """
    """
    try:
        if 'show' not in kwargs: show = False
        elif kwargs['show'] == False: show = False
        elif kwargs['show'] == True: show = True

        try:
            m = kwargs['m']
            n = kwargs['n']
        except KeyError:
            m, n = kwargs['L'], kwargs['L']

        try:
            i = kwargs['i']
            j = kwargs['j']
        except:
            i = kwargs['elem'][0]
            j = kwargs['elem'][1]

    except:
        print('Undeclared Dimension')
        exit(1)

    NW = ((m+i-1) % m, (n+j-1) % n)
    N = ((m+i-1) % m, j)
    NE = ((m+i-1) % m, (j+1) % n)

    W = (i, (n+j-1) % n)
    E = (i, (j+1) % n)

    SW = ((i+1) % m, (n+j-1) % n)
    S = ((i+1) % m, j)
    SE = ((i+1) % m, (j+1) % n)

    vicinity = {
        "NW": NW,
        "N": N,
        "NE": NE,
        "W": W,
        "E": E,
        "SW": SW,
        "S": S,
        "SE": SE,
    }

    if show:
        for k, v in vicinity.items():
            print(f'{k}: {v}')
    return vicinity


def countElem(conj, elem):
    if type(conj).__module__ == 'numpy':
        conj = conj.tolist()
    return count_nonzero(array(conj) == elem)
