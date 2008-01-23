#!/usr/bin/python
#
# Quantum Computing Python Library
# Copyright (C) 2008   Robert Nowotniak <robert@nowotniak.com>
#
#


from numpy import *


class QRegister:
    pass

class Qubit(QRegister):
    pass


class QCircuit:
    def __init__(self, *stages):
        self.stages = stages

    def process(self, qreg):
        m = self.stages[0]
        for s in self.stages[1:]:
            m = m * s


class QGate:
    def __init__(self):
        pass

    def __mul__(self, arg2):
        pass


class Stage(QGate):
    def __init__(self, *gates):
        self.gates = gates
        m = self.gates[0].matrix
        for g in self.gates[1:]:
            m = kron(m, g.matrix)
        self.matrix = m

    def __mul__(self, arg2):
        if isinstance(arg2, QRegister):
        elif isinstance(arg2, Stage):
        else:
            raise Exception('Wrong type exception')



class AbstractQGate(QGate):
    pass

class Identity(AbstractQGate):
    def __init__(self, size = 2):
        self.matrix = eye(size)
        

class Hadamard(AbstractQGate):
    def __init__(self, size = 2):
        self.matrix = matrix([
            [1, 1],
            [1, -1]])



class CNot(AbstractQGate):
    def __init__(self):
        self.matrix = matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]])

class Not(AbstractQGate):
    def __init__(self):
        self.matrix = matrix([
            [0, 1],
            [1, 0]])

class WrongSizeException(Exception):
    def __str__(self):
        return 'Wrong size of quantum computing object'

ket0 = transpose(array([[1, 0]]))
ket1 = transpose(array([[0, 1]]))
s2 = sqrt(2) / 2

if __name__ == '__main__':
    circ = QCircuit(
            Stage(Identity(2), Hadamard()),
            Stage(CNot())
            )
    print circ.process(ket0)


