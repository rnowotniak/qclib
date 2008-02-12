#!/usr/bin/python

from qclib import *

circuit = (I ** Hadamard() ** I) * (I ** CNot()) * (CNot(0, 1) ** I)

result = circuit(ket0 ** ket0 ** ket0)

print result.dirac()
print result

