#!/usr/bin/python

from qclib import *
import sys

N = 2 ** 3

n = N - 3

steps = int(floor(math.pi * 1.0/(math.asin(sqrt(1.0 / N))) / 4))

print 'Total numer of steps: ' + str(steps)
print

# identity gate
I = Identity(N)

w0 = Ket(n)

# initial state of quantum register
phi0 = QRegister([ones(N) / sqrt(N)])

print phi0

sys.exit(0)


# computation matrices
A = I - 2 * outer(w0,w0)
B = 2 * outer(phi0, phi0) - I




