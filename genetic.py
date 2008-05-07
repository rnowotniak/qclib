#!/usr/bin/python

from numpy import *
from qclib import *


def phenotype(s, a, b):
    return a + 1.0 * int(s, 2) * (1.0 * (b - a) / (2**len(s) - 1))

print phenotype('001', 0, 10)


