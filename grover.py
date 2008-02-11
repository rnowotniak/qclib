#!/usr/bin/python
#
# Python implementation of Grover search algorithm
# Copyright (C) 2007   Robert Nowotniak <robert@nowotniak.com>
#

from numpy import *
import random, sys

set_printoptions(precision=4, threshold=10, edgeitems=5, linewidth=120, suppress=True)

# size of the search set
N = 2 ** 9

# index of the searched element (arbitrary value between 0 .. N - 1)
n = N - 3 # f(x) = 1 <=> x==n

# total number of steps (optimal success probability)
steps = int(floor(math.pi * 1.0/(math.asin(sqrt(1.0 / N))) / 4))

print 'Total numer of steps: ' + str(steps)
print

# identity matrix
I = identity(N)

w0 = transpose(array([zeros(N)]))
w0[n,0] = 1

# initial state of quantum register
phi0 = transpose([ones(N) / sqrt(N)])

# computation matrices
A = I - 2 * outer(w0,w0)
B = 2 * outer(phi0, phi0) - I

phi = phi0
step = 0

while step <= steps:
    print 'Step number: ' + str(step)
    print '----------------'
    print 'Probability of search success: ',
    print '%0.4f' % abs(float(phi[n]))**2
    print
    if step < steps:
        phi = dot(B, dot(A, phi))
    step += 1

print 'Final quantum register |phi> state: '
print phi
print

print 'Probability of search success: ',
print '%0.4f' % abs(float(phi[n]))**2

success = (random.random() < float(phi[n])**2)

print 'MEASUREMENT! -> ',
if success:
    print 'success.'
else:
    print 'failure.'


sys.stdin.readline()

