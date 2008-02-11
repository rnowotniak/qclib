#!/usr/bin/python

from qclib import *

epr = (Hadamard() ** I) * CNot()

print epr(ket0 ** ket0)

