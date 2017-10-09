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
bob = (S ** cnot) * (I ** Swap()) * (cnot2 ** I) * \
        (I ** Swap()) * (S ** I ** T) * (I ** Swap()) * (cnot2 ** I) * (I ** Swap())

input = psi ** ket0 ** ket0
qreg = alice(input)
cbits = qreg.measure(1, 2)
output = bob(qreg)

print cbits ** psi # expected cirtuit output
print output # teleporation circuit output

