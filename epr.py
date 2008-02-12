#!/usr/bin/python

from qclib import *

epr = (Hadamard() ** I) * CNot()

pair = epr(ket0 ** ket0)
print pair
print pair.dirac()

