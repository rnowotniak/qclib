#!/usr/bin/python
#
# Modified genetic algorithm for learning quantum operators
#
#   UNDERCONSTRAINDED CASE EXPERIMENT
#
# Copyright (C) 2008   Robert Nowotniak <robert@nowotniak.com>
#
# based on:
# J. Faber, R.N. Thess, and G. Giraldi. Learning linear operators by genetic algorithms
#


from numpy import *
from qclib import *
from randU2 import randU2, u2
from random import shuffle, choice
from operators import random_unitary_matrix
import sys

# quantum examples
X = matrix([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]])
Y = matrix([
    [s2,  0, 0, 0],
    [s2,  0, 0, 0],
    [ 0, s2, 1, 0],
    [ 0, s2, 0, 1]])

GOOD = matrix([
    [s2, 0, 1, 1],
    [s2, 0, -1, -1],
    [0, s2, 1, -1],
    [0, s2, -1, 1]])

def fitness(m):
    t = (m * X - Y)
    return float(abs(0.5 * (t * t.H).trace()))

# to jest gorsze
def fitness2(m):
    err = 0
    for i in xrange(X.shape[1]):
        err += sum(m * X[:,i] - Y[:,i]) / (m.shape[0] * X.shape[1])
    return exp(-err)

#fitness = fitness

iterations = 400
poplen = 100
pc = 0.85
pm = 0.95
ps = 0.3
elitism = 30
nm = 2
perturb = 0.01


# initial random population
population = []
for i in xrange(poplen):
    population.append(random_unitary_matrix(4, real = True))

print 'Initial population:'
for c in population:
    print c

best = None
best_val = None

f = open('log.txt', 'w')

for epoch in xrange(iterations):

    print 'epoch ' + str(epoch)

    # calculate fitness
    fvalues = []
    for i in xrange(poplen):
        fvalues.append(fitness(population[i]))
    # print fvalues, min(fvalues)

    if best == None or min(fvalues) < best_val:
        best_val = min(fvalues)
        best = population[fvalues.index(best_val)]

    f.write('%d %f %f %f %f\n' % (epoch, best_val, min(fvalues), max(fvalues), sum(fvalues) / len(fvalues)))

    newpop = []
    # elitism
    if elitism > 0:
        ranking = fvalues[:]
        ranking.sort()
        for e in xrange(elitism):
            newpop.append(population[fvalues.index(ranking[e])])
    # crossover
    while len(newpop) < poplen:
        par1 = population[fvalues.index(choice(ranking[:int(ps * poplen)]))]
        par2 = population[fvalues.index(choice(ranking[:int(ps * poplen)]))]
        if random() <= pc:
            for n in xrange(2):
                child = par1.copy()
                for i in xrange(child.shape[0]):
                    for j in xrange(child.shape[1]):
                        if random() < 0.5:
                            child[i,j] = par2[i,j]
                newpop.append(child)
        else:
            newpop.append(par1)
            newpop.append(par2)
    # mutation
    for p in xrange(len(newpop)):
        if random() < pm:
            m = newpop[p]
            mutated = []
            while len(mutated) < nm:
                # random indices
                i = choice(range(m.shape[0]))
                j = choice(range(m.shape[1]))
                if mutated.count((i,j)) > 0:
                    continue
                mutated.append((i,j))
                m[i,j] += 2 * perturb * random() - perturb
                if m[i,j] > 1:
                    m[i,j] = 1
                elif m[i,j] < -1:
                    m[i,j] = -1
    population = newpop


print 'Error:'
print best_val
print 'Expected:'
print GOOD
print 'Best found solution:'
print best
print 'Unitary?'
print best*best.H

f.close()

