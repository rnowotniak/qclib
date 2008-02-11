#!/usr/bin/python

from qclib import *

circ = (I ** Hadamard() ** I) * (I ** CNot()) * (CNot(0, 1) ** I)

print circ(ket0 ** ket0 ** ket0)

