#!/usr/bin/python

from numpy import *


S = (
        (1.0/sqrt(5) * transpose(matrix([2, 1])), 1.0/sqrt(10) * transpose(matrix([3, 1]))),
        (1.0/sqrt(20) * transpose(matrix([-2, 4])), 1.0/sqrt(40) * transpose(matrix([2, -6]))),
        )

print S[0][0]
print S[1][0]

print dot(transpose(S[0][0]), S[1][0])

def random_unitary_matrix(n):
    z = (random.randn(n,n) + 1j * random.randn(n,n)) / sqrt(2.0)
    # for real matrix
    # z = (random.randn(n,n) + 1j * random.randn(n,n)) / sqrt(2.0)
    q,r = linalg.qr(z)
    d = diagonal(r)
    ph = d / absolute(d)
    q = multiply(q, ph, q)
    return matrix(q)

a = random_unitary_matrix(3)
print a
print (abs(a*a.H - eye(3)) > 10e-6).any()

