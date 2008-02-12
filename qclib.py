#!/usr/bin/python
#
# Quantum Computing Python Library
# Copyright (C) 2008   Robert Nowotniak <robert@nowotniak.com>
#
# $Id$
#
# qclib is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# qclib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with qclib; if not, write to the Free Software


from numpy import *
from random import random
import copy


# for floating point operations, comparisons etc.
epsilon = 10e-6


class QRegister:
    '''Quantum register class'''

    def __init__(self, m = None):
        if m == None:
            return
        if isinstance(m, ndarray) or type(m) == type([]):
            m = matrix(m)
        if isinstance(m, matrix) and m.shape[0] == 1:
            m = transpose(m)
        if not isinstance(m, matrix) or m.shape[1] != 1:
            raise WrongSizeException
        self.matrix = m

    def __rmul__(self, arg1):
        # arg1 * self
        if type(arg1) not in [int, float, complex]:
            raise Exception()
        result = copy.deepcopy(self)
        result.matrix = arg1 * self.matrix
        return result

    def __add__(self, arg2):
        # self + arg2
        result = copy.deepcopy(self)
        result.matrix = self.matrix + arg2.matrix
        return result

    def __sub__(self, arg2):
        # self - arg2
        result = copy.deepcopy(self)
        result.matrix = self.matrix - arg2.matrix
        return result

    def __pow__(self, arg2):
        # self ** arg2
        result = QRegister()
        result.matrix = kron(self.matrix, arg2.matrix)
        return result

    def __cmp__(self, other):
        m1 = self.matrix
        if isinstance(other, (matrix, ndarray)):
            m2 = other
        elif isinstance(other, QRegister):
            m2 = other.matrix
        else:
            return -1
        try:
            if sum(abs(m1 - m2)) < epsilon:
                return 0
            else:
                return 1
        except Exception:
            raise WrongSizeException, \
                    'Comparison of different size quantum registers'

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
            qubits = range(int(math.log(self.matrix.size, 2)))
        qubits = list(qubits)
        qubits.sort()
        p = {} # results probabilities
        # number of possible measurement results
        nres = 2 ** len(qubits)
        # enumerate all posible results
        for i in xrange(nres):
            p[dec2bin(i, int(math.log(nres, 2)))[::-1]] = 0.0
        for i in xrange(self.matrix.size):
            # reversed binary representation of base vector
            revbin = dec2bin(i, int(math.log(self.matrix.size, 2)))[::-1]
            # reversed binary representation of selected qubits
            revsel = ''.join([revbin[q] for q in qubits])
            p[revsel] += float(abs(self.matrix[i]) ** 2)
        keys = p.keys()
        # accumulated probabilities
        last = p[keys[0]]
        for k in keys[1:]:
            p[k] += last
            last = p[k]
        p[keys[-1]] = 1.0
        # get the measurement result according to probabilities
        r = random()
        for k in keys:
            if r <= p[k]:
                result = k
                break
        # selective reset of amplitudes
        for i in xrange(self.matrix.size):
            revbin = dec2bin(i, int(math.log(self.matrix.size, 2)))[::-1]
            revsel = ''.join([revbin[q] for q in qubits])
            if revsel != result:
                self.matrix[i] = 0.0
        # normalize final state
        self.normalize()
        return Ket(int(result[::-1], 2), len(qubits))

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
    '''Qubit class'''

    def __init__(self, val):
        if not isinstance(val, int):
            return QRegister.__init__(self, val)
        self.size = 1
        if val == 0:
            self.matrix = transpose(matrix([[1, 0]]))
        elif val == 1:
            self.matrix = transpose(matrix([[0, 1]]))
        else:
            raise WrongSizeException

    def flip(self):
        tmp = self.matrix[0]
        self.matrix[0] = self.matrix[1]
        self.matrix[1] = tmp


class QCircuit:
    '''Quantum circuit class'''

    def __init__(self, *stages):
        self.stages = stages

    def __call__(self, qreg):
        # Efficient algorithm could be implemented here
        # Wissam A. Samad, Roy Ghandour, and Mohamad.
        # Memory efficient quantum circuit simulator based on linked list architecture
        result = copy.deepcopy(qreg)
        for s in self.stages:
            result = s(result)
        return result


class QGate:
    '''Quantum gate class'''

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
            try:
                result.matrix = dot(self.matrix, arg2.matrix)
            except:
                raise WrongSizeException, 'Wrong size of input register for this gate'
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

    def inverse(self):
        self.matrix = linalg.inv(self.matrix)
        return self


class Stage(QGate):
    '''Quantum computing stage -- a layer in circuit'''

    def __init__(self, *gates):
        self.gates = gates
        m = self.gates[0].matrix
        for g in self.gates[1:]:
            m = kron(m, g.matrix)
        self.matrix = m

#
# Elementary quantum gates
#

class AbstractQGate(QGate):
    pass

class Identity(AbstractQGate):
    def __init__(self, size = 1):
        self.matrix = eye(2 ** size)
        

class Hadamard(AbstractQGate):
    def __init__(self, size = 1):
        h2 = s2 * matrix([
            [1, 1],
            [1, -1]])
        m = h2
        for i in xrange(size - 1):
            m = kron(m, h2)
        self.matrix = m


class CNot(AbstractQGate):
    '''Controlled not gate'''

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
    '''Not gate'''

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
    '''Toffoli gate -- Controlled Controlled Not gate'''
    def __init__(self):
        self.matrix = matrix([
            [ 1,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  1,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  1,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  1,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  1,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  1,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  1],
            [ 0,  0,  0,  0,  0,  0,  1,  0]])


class Fredkin(AbstractQGate):
    '''Fredkin gate -- Controlled Swap gate'''
    def __init__(self):
        self.matrix = matrix([
            [ 1,  0,  0,  0,  0,  0,  0,  0],
            [ 0,  1,  0,  0,  0,  0,  0,  0],
            [ 0,  0,  1,  0,  0,  0,  0,  0],
            [ 0,  0,  0,  1,  0,  0,  0,  0],
            [ 0,  0,  0,  0,  1,  0,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  1,  0],
            [ 0,  0,  0,  0,  0,  1,  0,  0],
            [ 0,  0,  0,  0,  0,  0,  0,  1]])


class Swap(AbstractQGate):
    '''Qubits order swap gate'''
    def __init__(self):
        self.matrix = matrix([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]])


class Arbitrary(AbstractQGate):
    '''Quantum gate with arbitrary unitary matrix'''
    def __init__(self, m):
        m = matrix(m)
        if m.H * m != eye(m.shape[0]):
            raise Exception, 'Not unitary matrix for quantum gate'
        self.matrix = m


class WrongSizeException(Exception):
    def __str__(self):
        return 'Wrong size of quantum computing object'


def dec2bin(dec, length = None):
    """convert decimal value to binary string"""
    result = ''
    if dec < 0:
        raise ValueError, "Must be a positive integer"
    if dec == 0:
        result = '0'
        if length != None:
            result = result.rjust(length, '0')
        return result
    while dec > 0:
        result = str(dec % 2) + result
        dec = dec >> 1
    if length != None:
        result = result.rjust(length, '0')
    return result


def Ket(n, size = None):
    if (n == 0 or n == 1) and size == None:
        return Qubit(n)
    ket = QRegister()
    if size == None:
        size = int(floor(math.log(n, 2)) + 1)
    ket.matrix = transpose(matrix([zeros(2 ** size)]))
    ket.matrix[n] = 1
    return ket


def epr(qreg = Ket(0) ** Ket(0)):
    """Generate an EPR-pair for |00> input state"""
    circ = (Hadamard() ** I) * CNot()
    return circ(qreg)


ket0 = Ket(0)
ket1 = Ket(1)
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
    input = ket1 ** ket0 ** ket1
    print input.dirac()
    print circ(input).dirac()

