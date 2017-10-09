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
from random import random

def randU2():
    phi = 2 * pi * random() - pi
    theta = 2 * pi * random() - pi
    psi = 2 * pi * random() - pi
    alpha = 2 * pi * random() - pi
    return u2(phi, theta, psi, alpha)

def u2(phi, theta, psi, alpha):
    m1 = matrix([
        [exp(-1j * phi), 0],
        [0, exp(1j * phi)]])
    m2 = matrix([
        [cos(theta), sin(-theta)],
        [sin(theta), cos(theta)]])
    m3 = matrix([
        [exp(-1j * psi), 0],
        [0, exp(1j * psi)]])
    m4 = matrix([
        [exp(1j*alpha), 0],
        [0, exp(1j * alpha)]])
    return m1 * m2 * m3 * m4

U2 = randU2()

if __name__ == '__main__':
    print U2
    print U2*U2.H

