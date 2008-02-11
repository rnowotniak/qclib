#!/usr/bin/python
#
# Teleportation quantum circuit simulation proof-of-concept
# Copyright (C) 2008   Robert Nowotniak
#
# Based on:
# [Bras98] Gilles Brassard. Teleportation as a quantum computation. 1998
#


from numpy import *
from random import random
from math import *
import sys


s2 = sqrt(2) / 2

# basic quantum gates
H = s2 * array([
    [1, 1],
    [1,-1]])
CNot = array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]])
CNot2 = array([
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0]])
phasePi = array([
    [1,  0],
    [0, -1]
    ])
Not = array([
    [0, 1],
    [1, 0],
    ])
I = identity(2)
Swap = array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]])

# quantum gates for Brassard teleportation circuit
L = s2 * array([
    [ 1, -1],
    [ 1,  1],
    ])
R = s2 * array([
    [ 1,  1],
    [-1,  1],
    ])
S = array([
    [ 1j,  0],
    [ 0,   1],
    ])
T = array([
    [-1,   0],
    [ 0, -1j],
    ])


ket0 = transpose(array([[1, 0]]))
ket1 = transpose(array([[0, 1]]))

# state for teleportation
psi = array([
    [      2.0/7 * (cos(pi/2/9) + 1.0j*sin(pi/2/9)) ],
    [ sqrt(45)/7 * (cos(pi/3*2) + 1.0j*sin(pi/3*2)) ],
    ])

# print abs(psi[1,0])**2 + abs(psi[0,0])**2

qreg = kron(kron(psi, ket0), ket0)
# print qreg


stage1 = matrix(kron(kron(I, L), I))
stage2 = matrix(kron(I, CNot))
stage3 = matrix(kron(CNot, I))
stage4 = matrix(kron(kron(R, I), I))
circ1  = stage4 * stage3 * stage2 * stage1
output1 = dot(circ1, qreg)

print 'quantum state just before the measurement in the middle:'
print output1
print

# measure-and-resend qubits
p00 = abs(output1[0])**2 + abs(output1[1])**2
p01 = abs(output1[2])**2 + abs(output1[3])**2
p10 = abs(output1[4])**2 + abs(output1[5])**2
p11 = abs(output1[6])**2 + abs(output1[7])**2
r = random()
if r < p00:
    bits = '00'
    output1[2:8] = 0
elif r < p00 + p01:
    bits = '01'
    output1[0:2] = 0
    output1[4:8] = 0
elif r < p00 + p01 + p10:
    bits = '10'
    output1[0:4] = 0
    output1[6:8] = 0
else:
    bits = '11'
    output1[0:6] = 0
# normalize
length = sqrt(sum(array(abs(output1))**2))
output1 = matrix(array(output1) / length)
print 'quantum state after measurement:'
print output1
print
# end of measure-and-resend

stage5 = matrix(kron(S, CNot))
stage6a = matrix(kron(I, Swap))
stage6b = matrix(kron(CNot2, I))
stage6c = stage6a
stage6 = dot(dot(stage6a, stage6b), stage6c)
stage7 = matrix(kron(kron(S, I), T))
stage8 = stage6

circ2 = stage8 * stage7 * stage6 * stage5
output = dot(circ2, output1)
print 'Result of teleportation:'
print output
print

# print sum(array(abs(output1))**2)

if bits == '00':
    expected = kron(ket0, ket0)
elif bits == '01':
    expected = kron(ket0, ket1)
elif bits == '10':
    expected = kron(ket1, ket0)
elif bits == '11':
    expected = kron(ket1, ket1)

expected = kron(expected, psi)

print 'Expected final state:'
print expected
print

#print sum(array(abs(expected))**2)

