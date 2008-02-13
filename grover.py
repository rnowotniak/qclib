#!/usr/bin/python

from qclib import *
import sys

N = 2 ** 3

n = N - 3

steps = int(floor(math.pi * 1.0/(math.asin(sqrt(1.0 / N))) / 4))

print 'Total numer of steps: ' + str(steps)
print

# identity gate
I = Identity(3)

w0 = Ket(n)

# initial state of quantum register
phi0 = QRegister([ones(N) / sqrt(N)])

# computation gates
A = I - 2 * w0.outer(w0)
B = 2 * phi0.outer(phi0) - I

phi = phi0
step = 0

while step <= steps:
    print 'Step number: ' + str(step)
    print '----------------'
    print 'Probability of search success: ',
    print '%0.4f' % abs(float(phi.matrix[n]))**2
    print
    if step < steps:
        phi = B(A(phi))
    step += 1

print 'Final quantum register |phi> state: '
print phi
print

print 'Probability of search success: ',
print '%0.4f' % abs(float(phi.matrix[n]))**2
print 

print 'Correct element: ', n
print 'State after measurement: ', phi.measure().dirac(binary = False)

