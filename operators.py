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

from numpy import *
import sys


def random_unitary_matrix(n, real = False):
    if not real:
        z = (random.randn(n,n) + 1j * random.randn(n,n)) / sqrt(2.0)
    else:
        z = (random.randn(n,n)) / sqrt(2.0)
    q,r = linalg.qr(z)
    d = diagonal(r)
    ph = d / absolute(d)
    q = multiply(q, ph, q)
    return matrix(q)

# print random_unitary_matrix(3, real = True)
# 
# a = random_unitary_matrix(3, real = True)
# print a
# print (abs(a*a.H - eye(3)) > 10e-6).any()

