#!/usr/bin/python

from random import choice,randint
from qclib import *
import sys

class Node:
    def __init__(self, type, target, control):
        # T -- bramka Pi/8, czyli obracajaca o Pi/4
        self.type = type # T, H, I lub CNot
        self.target = target
        self.control = control

    def __repr__(self):
        return '(%s, %s, %s)' % (self.type, self.target, self.control)

def randNode(qubits = 3):
    return Node(
            choice(('I', 'H', 'T', 'CNot')), 
            ''.join([choice(['0', '1']) for x in xrange(qubits)]),
            ''.join([choice(['0', '1']) for x in xrange(qubits)]))

def randGenotype(qubits = 3, length = 4):
    result = []
    for i in xrange(length):
        result.append(randNode(qubits))
    return result

def phenotype(genotype):
    stages = []
    for n in genotype:
        qubits = len(n.target)
        trgt = int(n.target, 2) % qubits
        ctrl = int(n.control, 2) % qubits
        if n.type == 'CNot' and ctrl != trgt:
            cnot = CNot(ctrl, trgt)
            gates = [cnot]
            gates += [I] * (qubits - cnot.size)
            gates.reverse()
        else:
            gates = [I] * (qubits - trgt - 1)
            if n.type == 'H':
                gates.append(h)
            elif n.type == 'I':
                gates.append(I)
            elif n.type == 'CNot':
                gates.append(Not())
            elif n.type == 'T':
                gates.append(T)
            else:
                raise Exception()
            gates += [I] * (qubits - len(gates))
        s = Stage(*gates)
        stages.append(s)
    return QCircuit(*stages)

input = Ket(0, 3)
expected = s2 * Ket(0, 3) + s2 * Ket(7, 3)
qubits = 3

def fitness(indiv):
    output = indiv(input)
    return sum(abs(output.matrix - expected.matrix))

# gen = randGenotype(qubits=3, length=4)
# #gen.append(Node('CNot', '000', '001'))
# print gen
# phen = phenotype(gen)
# for s in phen.stages:
#     print 'stage:'
#     print s.gates
# 
# print expected.dirac()
# 
# output = phen(input)
# 
# print
# print output.dirac()
# print
# 
# error = sum(abs(output.matrix - expected.matrix))
# 
# print 'error:', error

poplen = 100
elitism = 15
nstages = 5
Ngen = 100
pc = 0.7
pm = 0.05

population = []
for i in xrange(poplen):
    population.append(randGenotype(qubits = qubits, length = nstages))

# population[572] = \
#     [Node('H', '001', '000'), Node('CNot', '000', '001'), Node('CNot', '010', '001')]

# foo = population[572]
# ph = phenotype(foo)
# print fitness(ph)
# sys.exit(0)

f = open('log.txt', 'w')

print population

best = None
best_val = None

for epoch in xrange(Ngen):
    print 'epoch ' + str(epoch)

    fvalues = []
    for i in xrange(poplen):
        fvalues.append(fitness(phenotype(population[i])))

    if best == None or min(fvalues) < best_val:
        best_val = min(fvalues)
        best = population[fvalues.index(best_val)]

    f.write('%d %f %f %f %f\n' % (epoch, best_val, min(fvalues), max(fvalues), sum(fvalues) / len(fvalues)))

    newpop = []
    # elitism
    if elitism > 0:
        ranking = {}
        for i in xrange(poplen):
            ranking[i] = fvalues[i]
        kvs = ranking.items()
        kvs = [(v,k) for (k,v) in kvs]
        kvs.sort()
        kvs = [(k,v) for (v,k) in kvs]
        for e in xrange(elitism):
            newpop.append(population[kvs[e][0]])

    # tournament selection
    while len(newpop) < poplen:
        i1 = choice(range(len(population)))
        while True:
            i2 = choice(range(len(population)))
            if i1 != i2:
                break
        while True:
            i3 = choice(range(len(population)))
            if i3 != i2 and i3 != i1:
                break
        if fvalues[i1] < min(fvalues[i2], fvalues[i3]):
            newpop.append(population[i1])
        elif fvalues[i2] < min(fvalues[i1], fvalues[i3]):
            newpop.append(population[i2])
        else:
            newpop.append(population[i3])

    # cross over

    toCrossover = []
    for n in xrange(poplen):
        if random() <= pc:
            toCrossover.append(n)
    if len(toCrossover) % 2 != 0:
        n = int(floor(random() * poplen))
        while toCrossover.count(n) > 0:
            n = int(floor(random() * poplen))
        toCrossover.append(n)

    # indices of already crossed-over genotypes
    done = []
    for n in xrange(len(toCrossover)):
        par1 = toCrossover[n]
        if done.count(par1) > 0:
            continue

        while True:
            par2 = choice(toCrossover)
            if done.count(par2) == 0:
                break

        # crossover type
        crosstype = choice(('gate', 'target', 'control'))

        if crosstype == 'gate':
            cp = randint(1, nstages - 1)
            child1 = population[par1][:cp] + population[par2][cp:]
            child2 = population[par2][:cp] + population[par1][cp:]
            # replace parents with the offspring
            population[par1] = child1
            population[par2] = child2
            done.append(par1)
            done.append(par2)
        elif crosstype == 'target':
            g1 = choice(population[par1])
            g2 = choice(population[par2])
            cp = randint(0, len(g1.target))
            # crossover target qubit binary strings
            child1 = g1.target[:cp] + g2.target[cp:]
            child2 = g2.target[:cp] + g1.target[cp:]
            g1.target = child1
            g2.target = child2
        elif crosstype == 'control':
            g1 = choice(population[par1])
            g2 = choice(population[par2])
            cp = randint(0, len(g1.control))
            # crossover control qubit binary strings
            child1 = g1.control[:cp] + g2.control[cp:]
            child2 = g2.control[:cp] + g1.control[cp:]
            g1.control = child1
            g2.control = child2

    # mutation
    for n in xrange(poplen):
        for gi in xrange(len(population[n])):
            if random() <= pm:
                population[n][gi] = randNode(qubits = qubits)

print best_val
print phenotype(best)

f.close()

