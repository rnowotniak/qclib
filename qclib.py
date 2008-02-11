#!/usr/bin/python
#
# Quantum Computing Python Library
# Copyright (C) 2008   Robert Nowotniak <robert@nowotniak.com>
#
#

from numpy import *
import copy

class QRegister:
    def __rmul__(self, arg1):
        # arg1 * self
        if type(arg1) not in [int, float]:
            raise Exception()
        result = copy.deepcopy(self)
        result.matrix = arg1 * self.matrix
        return result
    def __add__(self, arg2):
        # self + arg2
        result = copy.deepcopy(self)
        result.matrix = self.matrix + arg2.matrix
        return result
    def __pow__(self, arg2):
        # self ** arg2
        result = QRegister()
        result.matrix = kron(self.matrix, arg2.matrix)
        return result
    def __str__(self):
        return str(self.matrix)
    def normalize(self):
        l = sqrt(sum([abs(x)**2 for x in self.matrix]))
        self.matrix = l * self.matrix
        return self
    def measure(self, *qubits):
        pass


class Qubit(QRegister):
    def __init__(self, val):
        self.size = 2
        if val == 0:
            self.matrix = transpose(array([[1, 0]]))
        elif val == 1:
            self.matrix = transpose(array([[0, 1]]))
        else:
            raise Exception()


class QCircuit:
    def __init__(self, *stages):
        self.stages = stages

    def __call__(self, qreg):
        # tu mozna uwzglednic wydajny algorytm (memory)
        result = copy.deepcopy(qreg)
        for s in self.stages:
            result = s(result)
        return result




class QGate:
    def __init__(self):
        pass

    def __pow__(self, arg2):
        # polaczenie rownolegle bramek
        if not isinstance(arg2, QGate):
            raise Exception(repr(arg2))
        result = Stage(self, arg2)
        return result
    def __str__(self):
        return str(self.matrix)
    def __mul__(self, arg2):
        # self * arg2
        if isinstance(arg2, QRegister):
            # gate * reg
            result = QRegister()
            result.matrix = dot(self.matrix, arg2.matrix)
            return result
        if self.matrix.shape != arg2.matrix.shape:
            raise Exception()
        # gate * gate
        result = QGate()
        # order changed!
        result.matrix = dot(arg2.matrix, self.matrix)
        return result
    def __call__(self, qreg):
        if not isinstance(qreg, QRegister):
            raise Exception()
        return self * qreg


class Stage(QGate):
    def __init__(self, *gates):
        self.gates = gates
        m = self.gates[0].matrix
        for g in self.gates[1:]:
            m = kron(m, g.matrix)
        self.matrix = m


class AbstractQGate(QGate):
    pass

class Identity(AbstractQGate):
    def __init__(self, size = 2):
        self.matrix = eye(size)
        

class Hadamard(AbstractQGate):
    def __init__(self, size = 2):
        self.matrix = s2 * matrix([
            [1, 1],
            [1, -1]])



class CNot(AbstractQGate):
    def __init__(self, control = 1, target = 0):
        if control not in (0, 1) or target not in (1, 0) or control == target:
            raise Exception()
        if control == 1 and target == 0:
            self.matrix = matrix([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 1],
                [0, 0, 1, 0]])
        elif control == 0 and target == 1:
            self.matrix = matrix([
                [1, 0, 0, 0],
                [0, 0, 0, 1],
                [0, 0, 1, 0],
                [0, 1, 0, 0]])

class Not(AbstractQGate):
    def __init__(self):
        self.matrix = matrix([
            [0, 1],
            [1, 0]])

class Swap(AbstractQGate):
    def __init__(self):
        self.matrix = matrix([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]])


class WrongSizeException(Exception):
    def __str__(self):
        return 'Wrong size of quantum computing object'

ket0 = Qubit(0)
ket1 = Qubit(1)
s2 = sqrt(2) / 2

h2 = Hadamard()
I = Identity()
cnot = CNot()
cnot2 = CNot(0, 1)

if __name__ == '__main__':
    import sys
    
    # kety bazy standardowej
    print ket0
    print ket1

    # arbitralne stany kubitow
    print 0.3 * ket0
    print 0.4 * ket0 + 0.5 * ket1
    print (0.4 * ket0 + 0.5 * ket1).normalize()
    print repr(0.4 * ket0 + 0.5 * ket1)
    print repr(ket0)

    # iloczyn tensorowy kubitow i rej kwantowych
    print ket0 ** ket0
    print ket0 ** ket1
    print ket1 ** ket1
    print repr(ket1 ** ket1)
    print ket0 ** ket1 ** ket0
    print repr(ket0 ** ket1 ** ket0)

    # bramki elementarne
    h2 = Hadamard()
    I = Identity()
    cnot = CNot()
    print h2
    print I
    print cnot
    print repr(cnot)

    # mnozenie bramek
    print h2 * I

    # iloczyn tensorowy bramek
    print h2 ** cnot
    print h2 ** cnot ** cnot

    # dzialanie bramka na rejestr lub kubit
    print h2 * I
    print h2 * ket0
    print h2 * ket1

    # calling gates like functions
    print h2(ket0)

    print 
    cnot2 = CNot(0, 1)
    circ = (I ** h2 ** I) * (I ** cnot) * (cnot2 ** I)
    print circ(ket0 ** ket0 ** ket0)
    circ = QCircuit(
            Stage(I, h2, I),
            Stage(I, cnot),
            Stage(cnot2, I)
    )
    print circ(ket0 ** ket0 ** ket0)

    print 
    input = ket0 ** ket0 ** ket0
    circ = (I ** h2 ** I) * (I ** cnot) * (cnot2 ** I)
    print circ(input)

    print
    print 'swap test, niesasiadujace kubity, test z cnot2'
    circ = (I ** Swap()) * (cnot2 ** I) * (I ** Swap())
    print circ
    print circ(ket1 ** ket0 ** ket1)

