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
import sys

N = 2 ** 3

n = N - 3

steps = int(floor(math.pi * 1.0/(math.asin(sqrt(1.0 / N))) / 4))

print 'Total numer of steps: ' + str(steps)
print

# identity gate
I = Identity(3)

w0 = Ket(n)

# initial state of quantum register
phi0 = QRegister([ones(N) / sqrt(N)])

# computation gates
A = I - 2 * w0.outer(w0)
B = 2 * phi0.outer(phi0) - I

phi = phi0
step = 0

print A*B

while step <= steps:
    print 'Step number: ' + str(step)
    print '----------------'
    print 'Probability of search success: ',
    print '%0.4f' % abs(float(phi.matrix[n]))**2
    print
    if step < steps:
        phi = B(A(phi))
    step += 1

print 'Final quantum register |phi> state: '
print phi
print

print 'Probability of search success: ',
print '%0.4f' % abs(float(phi.matrix[n]))**2
print 

print 'Correct element: ', n
print 'State after measurement: ', phi.measure().dirac(binary = False)

