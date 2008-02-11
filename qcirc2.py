#!/usr/bin/python
#
# Simulation of quantum circuit generating maximally entangled 3-qubit quantum register
# Copyright (C) 2007   Robert Nowotniak
#
#
# Memory-efficient, smart approach of performing matrix operations,
# as presented in:
#
# [SGC]
#    Wissam Abdel Samad, Roy Ghandour, Mohamad Nabil Hajj Chehade
#    Memory Efficient Quantum Circuit Simulator Based on Linked List Architecture
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
import sys

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

# for circuit output testing purposes
I2 = array([
    [1, 0],
    [0, 1]])

# initial state |000>
input = transpose(array([[1,0,0,0,0,0,0,0]]))

# Smart computing of stage outputs
i = 0
output1 = []
for l1 in xrange(I.shape[0]):
    for l2 in xrange(h.shape[0]):
        for l3 in xrange(I2.shape[0]):
            c = kron(kron(I[l1], h[l2]), I2[l3])
            r = dot(c, input)
            output1.append(r[0])
            # print l1, l2, l3, r,
            # print
            i += 1
output1 = transpose([array(output1)])
# print output1

# print 'second stage:'

output2 = []
for l1 in xrange(I.shape[0]):
    for l2 in xrange(xor.shape[0]):
        c = kron(I[l1], xor[l2])
        r = dot(c, output1)
        output2.append(r[0])
        # print l1, l2, r,
        # print
        i += 1
output2 = transpose([array(output2)])
# print output2

# print 'third stage:'

output3 = []
for l1 in xrange(xor2.shape[0]):
    for l2 in xrange(I.shape[0]):
        c = kron(xor2[l1], I[l2])
        r = dot(c, output2)
        output3.append(r[0])
        # print l1, l2, r,
        # print
        i += 1
output3 = transpose([array(output3)])

print 'efficient method result:'
print output3


print 'expected results:'

#
# Matrix of individual stage is a Kronecker (tensor) product of parallel gates
# Notice that the more significant qubit have to be the first factor
#

# matrix for first stage of computation
stage1 = kron(kron(I,h),I2)
# print dot(stage1, input)

stage2 = kron(I,xor)
# print dot(stage2, dot(stage1, input))

stage3 = kron(xor2,I)

# expected circuit output
print dot(stage3, dot(stage2, dot(stage1, input)))

