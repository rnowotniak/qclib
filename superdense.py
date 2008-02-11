#!/usr/bin/python
#
# Superdense coding quantum circuit proof-of-concept
# Copyright (C) 2007   Robert Nowotniak
#


from numpy import *
from math import *
import sys


# basic quantum gates
h = sqrt(2) / 2 * array([
    [1, 1],
    [1,-1]])
CNot = array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]])
phasePi = array([
    [1,  0],
    [0, -1]
    ])
Not = array([
    [0, 1],
    [1, 0],
    ])
I = identity(2)

# quantum gate for superdense coding
s2 = sqrt(2) / 2
B = array([
    [s2,   0,  0,  s2],
    [ 0,  s2, s2,   0],
    [s2,   0,  0, -s2],
    [ 0, -s2, s2 ,  0],
    ])


# bits for coding
b1 = 1
b2 = 1

print 'Bits: ', b1, b2
print


# initial state |00>
qreg = transpose([[1, 0, 0, 0]])

# create entangled EPR pair of qubits
qreg = dot(dot(CNot, kron(h, I)), qreg)

# entangled state of two qubits:  sqrt(2)/2 ( |00> + |11> )
print 'Entangled pair: sqrt(2)/2 (|00> + |11>):'
print qreg
print


# Perform coding operations on Alice qubit
if b1:
    qreg = dot(kron(phasePi, I), qreg)

if b2:
    qreg = dot(kron(Not, I), qreg)

print 'State after Alice operations:'
print qreg
print 

qreg = dot(B, qreg)

print qreg
print


