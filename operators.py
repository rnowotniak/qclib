#!/usr/bin/python

from numpy import *
import sys


def random_unitary_matrix(n, real = False):
    if not real:
        z = (random.randn(n,n) + 1j * random.randn(n,n)) / sqrt(2.0)
    else:
        z = (random.randn(n,n)) / sqrt(2.0)
    q,r = linalg.qr(z)
    d = diagonal(r)
    ph = d / absolute(d)
    q = multiply(q, ph, q)
    return matrix(q)

print random_unitary_matrix(3, real = True)

a = random_unitary_matrix(3, real = True)
print a
print (abs(a*a.H - eye(3)) > 10e-6).any()

