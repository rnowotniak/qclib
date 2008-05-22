#!/usr/bin/python

from numpy import *
from qclib import *
import sys

len1 = 2
len2 = 3

plik = file('sup2.txt', 'w')

foo = []
for c in list('IHNT'):
    for i in xrange(2):
        for j in xrange(4):
            foo.append('%c%d%d' % (c, i, j))

#foo = list('0123456789')

def allenc(dep, prefix = ''):
    if dep == 1:
        for zz in foo:
            plik.write(prefix + zz + '\n')
    elif dep > 1:
        for zz in foo:
            allenc(dep - 1, prefix + zz)

allenc(8)

plik.close()

sys.exit(0)

bar = []
for c in list('IHNT'):
    for i in xrange(4):
        for j in xrange(4):
            bar.append('%c%d%d' % (c, i, j))

foo = list('abc')
bar = list('01')

def foobar(dep1, dep2, cur = ''):
    if dep1 == 1 and dep2 == 1:
        for zz in foo:
            for ww in bar:
                print cur + zz + ww
        return
    if dep2 > 1:
        for aa in xrange(dep2):
            for ww in bar:
                foobar(dep1, dep2 - 1, ww)

foobar(1,2)

sys.exit(0)

gset = ('I', 'H', 'Not', 'T')
pset1 = (0, 1)
pset2 = (0, 1, 2, 3)

class Solution:
    def __init__(self):
        g = []
        for i in xrange(len1):
            g.append([gset[0], pset1[0], pset2[0]])
        # encoding stage genotype
        self.encgen = g
        g = []
        for i in xrange(len2):
            g.append([gset[0], pset2[0], pset2[0]])
        # decoding stage genotype
        self.decgen = g

    def genotype(self):
        return self.encgen + self.decgen

    def next(self):
        changed = False
        for i in self.encgen:
            if i[0] == 'I':
                i[0] = 'H'
                changed = True
            elif i[0] == 'H':
                i[0] = 'Not'
                changed = True
            elif i[0] == 'Not':
                i[0] = 'T'
                changed = True
            elif i[1] == 0:
                i[1] = 1
                changed = True
            elif i[2] < 3:
                i[2] += 1
                changed = True
            if changed:
                break
        if not changed:
            for i in self.decgen:
                if i[0] == 'I':
                    i[0] = 'H'
                    changed = True
                elif i[0] == 'H':
                    i[0] = 'Not'
                    changed = True
                elif i[0] == 'Not':
                    i[0] = 'T'
                    changed = True
                elif i[1] < 3:
                    i[1] += 1
                    changed = True
                elif i[2] < 3:
                    i[2] += 1
                    changed = True
                if changed:
                    break
            if not changed:
                raise Exception('not more solutions')

s = Solution()
print s.genotype()

for x in xrange(6):
    s.next()
print s.genotype()

