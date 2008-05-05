#!/usr/bin/python

from numpy import *
from random import random

phi = random()
theta = random()
psi = random()
alpha = random()

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

U2 = m1 * m2 * m3 * m4

print U2*U2.H

