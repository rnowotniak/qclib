#!/usr/bin/python
#
# Quantum Computing Python Library
# Copyright (C) 2008   Robert Nowotniak <robert@nowotniak.com>
#
#

from numpy import *
from random import random
import copy

epsilon = 10e-6

def dec2bin(dec):
    """convert decimal value to binary string"""
    result = ""
    if dec < 0:
        raise ValueError, "Must be a positive integer"
    if dec == 0:
        return '0'
    while dec > 0:
        result = str(dec % 2) + result
        dec = dec >> 1
    return result

def Ket(n):
    if n == 0 or n == 1:
        return Qubit(n)
    ket = QRegister()
    ket.matrix = transpose(matrix([zeros(2**int(floor(math.log(n, 2)) + 1))]))
    ket.matrix[n] = 1
    return ket

class QRegister:
    def __init__(self, m = None):
        if m == None:
            return
        if isinstance(m, ndarray):
            m = matrix(m)
        if isinstance(m, matrix) and m.shape[0] == 1:
            m = transpose(m)
        if not isinstance(m, matrix) or m.shape[1] != 1:
            raise WrongSizeException
        self.matrix = m
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
    def reset(self, n = 0):
        for i in xrange(self.matrix.size):
            self.matrix[i] = 0
        self.matrix[n] = 1
    def normalize(self):
        l = sqrt(sum([abs(x)**2 for x in self.matrix]))
        self.matrix = self.matrix / l
        return self
    def measure(self, *qubits):
        if len(qubits) == 0:
            # measure all qubits in register
            pass
        else:
            raise Exception, 'Not implemented yet'
        r = random()
        p = [float(x) for x in array(abs(self.matrix)) ** 2]
        # acumulated values
        for i in xrange(1,len(p)):
            p[i] += p[i - 1]
        for i in xrange(len(p)):
            if r < p[i]:
                break
        self.reset(i)
        return self
    def dirac(self, reduce = True, binary = True):
        """Return state in Dirac (bra-ket) notation"""
        elems = []
        if len(filter(lambda x: float(abs(x)) > 1 - epsilon, self.matrix)) == 1:
            single = True
        else:
            single = False
        for i in xrange(self.matrix.size):
            val = complex(real(self.matrix[i]), imag(self.matrix[i]))
            if reduce and abs(val) < epsilon:
                continue
            if abs(val) < epsilon:
                elem = '+0'
            elif imag(val) == 0:
                elem = '%+g' % abs(val)
            elif real(val) != 0:
                elem = '+%s' % str(val)
            else:
                # only imaginary part
                elem = '%+gj' % (imag(val))
            if single and reduce:
                elem = ''
            if binary:
                elem += ('|%0'+str(math.log(self.matrix.size, 2))+'d>') % int(dec2bin(i))
            else:
                elem += '|%s>' % i
            elems.append(elem)
        return ' '.join(elems)


class Qubit(QRegister):
    def __init__(self, val):
        self.size = 2
        if val == 0:
            self.matrix = transpose(matrix([[1, 0]]))
        elif val == 1:
            self.matrix = transpose(matrix([[0, 1]]))
        else:
            raise WrongSizeException


class QCircuit:
    def __init__(self, *stages):
        self.stages = stages

    def __call__(self, qreg):
        # tu mozna uwzglednic wydajny algorytm
        # Wissam A. Samad, Roy Ghandour, and Mohamad.
        # Memory efficient quantum circuit simulator based on linked list architecture
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
    def trace(self):
        return self.matrix.trace()
    def determinant(self):
        return linalg.det(self.matrix)
    def transpose(self):
        self.matrix = transpose(self.matrix)
        return self
    def inverse(self)
        self.matrix = linalg.inv(self.matrix)
        return self


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

class PhaseShift(AbstractQGate):
    def __init__(self, angle = pi):
        self.angle = angle
        self.matrix = matrix([
            [1, 0],
            [0, exp(angle * 1j)]])

class Toffoli(AbstractQGate):
    pass

class Fredkin(AbstractQGate):
    pass

class Swap(AbstractQGate):
    def __init__(self):
        self.matrix = matrix([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]])

class Arbitrary(AbstractQGate):
    def __init__(self, m):
        self.matrix = matrix(m)


ket0 = Qubit(0)
ket1 = Qubit(1)
s2 = sqrt(2) / 2

def epr(qreg = ket0 ** ket0):
    """Generate an EPR-pair for |00> input"""
    circ = (Hadamard() ** I) * CNot()
    return circ(qreg)



class WrongSizeException(Exception):
    def __str__(self):
        return 'Wrong size of quantum computing object'


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
    input = ket1 ** ket0 ** ket1
    print input.dirac()
    print circ(input).dirac()

