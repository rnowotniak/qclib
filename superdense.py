#!/usr/bin/python

from qclib import *

qreg = epr()

b1 = 1
b2 = 1

# Perform coding operations on Alice qubit
if b1:
    qreg = (PhaseShift(pi) ** I)(qreg)

if b2:
    qreg = (Not() ** I)(qreg)

B = Arbitrary(matrix([
    [s2,   0,  0,  s2],
    [ 0,  s2, s2,   0],
    [s2,   0,  0, -s2],
    [ 0, -s2, s2 ,  0],
    ]))

print B(qreg).dirac()



