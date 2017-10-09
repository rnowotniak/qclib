#!/usr/bin/python
#
# Genetic Programming algorithm for for evolving
# 5-qubit entanglement production quantum circuit
#
# Copyright (C) 2006   Robert Nowotniak <rnowotniak@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# based on:
# [Rub00] Ben I. P. Rubinstein. Evolving quantum circuits using genetic programming
#

from random import choice,randint
from qclib import *
from copy import deepcopy as dc
import sys


class Node:
    ''' Genetic Programming Tree Node '''

    def __init__(self, type, target, control):
        self.type = type # T, H, I lub CNot
        # T --  Pi/8 gates (shifts the phase with the Pi/4 angle)
        self.target = target
        self.control = control

    def __repr__(self):
        return '(%s, %s, %s)' % (self.type, self.target, self.control)

def randNode(qubits = 3):
    ''' Generate random GP Tree Node '''
    return Node(
            choice(('I', 'H', 'T', 'CNot')), 
            ''.join([choice(['0', '1']) for x in xrange(qubits)]),
            ''.join([choice(['0', '1']) for x in xrange(qubits)]))

def randGenotype(qubits = 3, length = 4):
    ''' Generate random genotype (GP Tree) '''
    result = []
    for i in xrange(length):
        result.append(randNode(qubits))
    return result

def phenotype(genotype):
    ''' Transforms genotype into phenotypes (QCircuits) space '''
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

input = Ket(0, 5)  # |00000>
expected = s2 * Ket(0, 5) + s2 * Ket(31, 5)
qubits = 5

def fitness(indiv):
    output = indiv(input)
    return sum(abs(output.matrix - expected.matrix))

poplen = 500
elitism = 10
nstages = 5
Ngen = 70
pc = 0.75
pm = 0.05
nm = 1

# Generate random population
population = []
for i in xrange(poplen):
    population.append(randGenotype(qubits = qubits, length = nstages))

###
# just a test..
CHEAT = [
        Node('H', '11111', '11011'),
        Node('CNot', '01001', '10101'),
        Node('CNot', '10010', '00001'),
        Node('CNot', '11011', '01011'),
        Node('CNot', '11001', '01001')]
###

f = open('log.txt', 'w')

print population

best = None
best_val = None

for epoch in xrange(Ngen):
    print 'epoch ' + str(epoch)
    sys.stdout.flush()

    ###
    if epoch == 2 and CHEAT != None:
        population[randint(0,len(population)-1)] = CHEAT
    ###

    fvalues = []
    for i in xrange(poplen):
        fvalues.append(fitness(phenotype(population[i])))

    # for roulette selection
    sects = [-v for v in fvalues]
    m = min(sects)
    if m < 0:
        sects = [s - m + (0.01 * abs(m)) for s in sects]
    sects /= sum(sects)
    # accumulated probabilities
    for i in xrange(1, poplen):
        sects[i] = sects[i - 1] + sects[i]
    sects[-1] = 1.0

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
            newpop.append(dc(population[kvs[e][0]]))

    while len(newpop) < poplen:
        # select genetic operation probabilistically
        r = random()
        if r <= pm:
            op = 'mutation'
        elif r <= pm + pc:
            op = 'crossover'
        else:
            op = 'reproduction'

        # select two individuals by roulette
        r = random()
        for j in xrange(len(sects)):
            if r <= sects[j]:
                indiv1 = j
                break
        r = random()
        for j in xrange(len(sects)):
            if r <= sects[j]:
                indiv2 = j
                break

        if op == 'reproduction':
            newpop.append(dc(population[indiv1]))
        elif op == 'crossover':

            par1 = indiv1
            par2 = indiv2

            # crossover type
            crosstype = choice(('gate', 'target', 'control'))

            if crosstype == 'gate':
                cp = randint(1, nstages - 1)
                child1 = dc(population[par1][:cp] + population[par2][cp:])
                child2 = dc(population[par2][:cp] + population[par1][cp:])
            elif crosstype == 'target':
                child1 = dc(population[par1])
                child2 = dc(population[par2])
                g1 = choice(child1)
                g2 = choice(child2)
                cp = randint(0, len(g1.target))
                # crossover target qubit binary strings
                control1 = g1.target[:cp] + g2.target[cp:]
                control2 = g2.target[:cp] + g1.target[cp:]
                g1.target = control1
                g2.target = control2
            elif crosstype == 'control':
                child1 = dc(population[par1])
                child2 = dc(population[par2])
                g1 = choice(child1)
                g2 = choice(child2)
                cp = randint(0, len(g1.control))
                # crossover control qubit binary strings
                target1 = g1.target[:cp] + g2.target[cp:]
                target2 = g2.target[:cp] + g1.target[cp:]
                g1.target = target1
                g2.target = target2
            else:
                assert(False)
            # add the offspring to new population
            newpop.append(child1)
            newpop.append(child2)
        elif op == 'mutation':
            # mutation
            child = dc(population[indiv1])
            done = []
            for i in xrange(nm):
                while True:
                    gi = choice(xrange(len(child)))
                    if gi not in done:
                        break
                done.append(gi)
                child[gi] = randNode(qubits = qubits)
            newpop.append(child)
        else:
            # NOT REACHABLE
            assert(False)

    population = newpop

print 'error:', best_val
print best

f.close()

