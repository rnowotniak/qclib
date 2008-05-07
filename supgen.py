#!/usr/bin/python

from qclib import *


B = Arbitrary([
    [s2,   0,  0,  s2],
    [ 0,  s2, s2,   0],
    [s2,   0,  0, -s2],
    [ 0, -s2, s2 ,  0],
    ])

print B

