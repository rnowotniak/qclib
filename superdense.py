#!/usr/bin/python
#
# qclib - Quantum Computing library for Python
# Copyright (C) 2006   Robert Nowotniak <rnowotniak@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from qclib import *

qregiter = epr()

b1 = 1
b2 = 0

# Perform coding operations on Alice qubit
if b1:
    print (PhaseShift(pi) ** I)
    qregiter = (PhaseShift(pi) ** I)(qregiter)

if b2:
    qregiter = (Not() ** I)(qregiter)

B = Arbitrary([
    [s2,   0,  0,  s2],
    [ 0,  s2, s2,   0],
    [s2,   0,  0, -s2],
    [ 0, -s2, s2 ,  0],
    ])

print B(qregiter).dirac()



