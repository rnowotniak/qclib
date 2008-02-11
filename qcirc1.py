#!/usr/bin/python
#
# Simulation of quantum circuit generating maximally entangled 3-qubit quantum register
# Copyright (C) 2007   Robert Nowotniak
#
#
# Circuit diagram:
#
#      --------+--   3rd qubit
#              |
#      --H--.--.--   2nd qubit
#           |
#      -----+-----   1st qubit
#
# The circuit is composed of three stages:
#    Hadamard transform on the 2nd qubit
#    Controlled-Not on the 1st (target) and 2nd (control) qubit
#    Controlled-Not on the 3st (target) and 2nd (control) qubit
#
# For the input quantum register |000>, output of the circuit is in
# maximally entangled form:
#    sqrt(2) / 2 * ( |000> + |111> )
#


from numpy import *
from math import *

xor = array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]])

xor2 = array([
    [1, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0]])

# H1 Hadamard transform
h = sqrt(2) / 2 * array([
    [1, 1],
    [1,-1]])

# Identity matrix
I = array([
    [1, 0],
    [0, 1]])

# initial state |000>
input = transpose(array([[1,0,0,0,0,0,0,0]]))

#
# Matrix of individual stage is a Kronecker (tensor) product of parallel gates
# Notice that the more significant qubit have to be the first factor
#

# matrix for first stage of computation
stage1 = kron(kron(I,h),I)

# matrix for second stage of computation
stage2 = kron(I,xor)

# matrix for third stage of computation
stage3 = kron(xor2,I)


# Circuit matrix - matrix product of all stages
#    (S3 S2 S1) |psi> 
circuit = dot(dot(stage3, stage2), stage1)

output = dot(circuit, input)

print 'Initial quantum register state:'
print str(input)
print

print 'Output quantum register state:'
print str(output)
print

