#!/usr/bin/python

from qclib import *

# quantum gates for Brassard teleportation circuit
L = Arbitrary(s2 * array([
    [ 1, -1],
    [ 1,  1],
    ]))
R = Arbitrary(s2 * array([
    [ 1,  1],
    [-1,  1],
    ]))
S = Arbitrary([
    [ 1j,  0],
    [ 0,   1],
    ])
T = Arbitrary([
    [-1,   0],
    [ 0, -1j],
    ])

psi = Qubit([
    [      2.0/7 * (cos(pi/2/9) + 1.0j*sin(pi/2/9)) ],
    [ sqrt(45)/7 * (cos(pi/3*2) + 1.0j*sin(pi/3*2)) ],
    ])


alice = (I ** L ** I) * (I ** cnot) * (cnot ** I) * (R ** I ** I)
bob = (S ** cnot) * (I ** Swap()) * (cnot2 ** I) * (I ** Swap()) * (S ** I ** T) * (I ** Swap()) * (cnot2 ** I) * (I ** Swap())

input = psi ** ket0 ** ket0
qreg = alice(input)
cbits = qreg.measure(1, 2)
output = bob(qreg)

print cbits ** psi # expected cirtuit output
print output # teleporation circuit output

