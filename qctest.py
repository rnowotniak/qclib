#!/usr/bin/python
# -*- coding: iso8859-2 -*-
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


import unittest
import sys

from qclib import *

class QclibTestCase(unittest.TestCase):
    def runTest(self):
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
        h = Hadamard()
        I = Identity()
        cnot = CNot()
        print h
        print I
        print cnot
        print repr(cnot)

        # mnozenie bramek
        print h * I

        # iloczyn tensorowy bramek
        print h ** cnot
        print h ** cnot ** cnot

        # dzialanie bramka na rejestr lub kubit
        print h * I
        print h * ket0
        print h * ket1

        # calling gates like functions
        print h(ket0)

        print 
        cnot2 = CNot(0, 1)
        circ = (I ** h ** I) * (I ** cnot) * (cnot2 ** I)
        print circ(ket0 ** ket0 ** ket0)
        circ = QCircuit(
                Stage(I, h, I),
                Stage(I, cnot),
                Stage(cnot2, I)
        )
        print circ(ket0 ** ket0 ** ket0)

        print 
        input = ket0 ** ket0 ** ket0
        circ = (I ** h ** I) * (I ** cnot) * (cnot2 ** I)
        print circ(input)

        print
        print 'swap test, niesasiadujace kubity, test z cnot2'
        circ = (I ** Swap()) * (cnot2 ** I) * (I ** Swap())
        print circ
        input = ket1 ** ket0 ** ket1
        print input.dirac()
        print circ(input).dirac()


class QuantumCircuitTestCase(unittest.TestCase):
    pass

class QubitTestCase(unittest.TestCase):
    """A test case for Qubit class"""

    def setUp(self):
        self.q1 = (0.3 * ket0 + 0.4 * ket1).normalize()

    def testQubit(self):
        print self.q1

    def testFlip(self):
        pass


class QRegisterTestCase(unittest.TestCase):
    """A test case for QRegister class"""

    def setUp(self):
        self.q1 = (0.3 * ket0 + 0.4 * ket1).normalize()
        self.q2 = (0.5 * ket0 + 0.333 * ket1).normalize()
        self.q3 = ((0.3j + 0.7) * ket0 + (0.4 + 0.1j) * ket1).normalize()

    def testNormalize(self):
        q1 = (0.3 * ket0 + 0.4 * ket1).normalize()
        q2 = (0.5 * ket0 + 0.333 * ket1).normalize()
        q3 = ((0.3j + 0.7) * ket0 + (0.4 + 0.1j) * ket1).normalize()
        for q in (q1, q2, q3):
            assert abs(sum(array(abs(q.matrix)) ** 2) - 1) < epsilon, \
                    'Not normalized state'

    def testKets(self):
        pass

    def testTensor(self):
        pass

    def testGates(self):
        pass

    def testDirac(self):
        assert ket0.dirac() == '|0>'
        assert ket1.dirac() == '|1>'
        assert (ket0**ket1).dirac() == '|01>'

    def testEpr(self):
        inp = ket0 ** ket0
        pair = epr(inp)
        assert sum(abs(pair.matrix - transpose(matrix([sqrt(2)/2, 0, 0, sqrt(2)/2])))) < epsilon, \
                'Not an EPR pair'

    def testKet(self):
        print (Ket(5) + Ket(6)).normalize().dirac()

    def testMeasureAll(self):
        assert ket0.measure() == ket0
        assert ket1.measure() == ket1
        res = [0, 0]
        for i in xrange(100):
            q = (ket0 + ket1).normalize()
            q.measure()
            if q == ket0:
                res[0] += 1
            elif q == ket1:
                res[1] += 1
            else:
                self.fail('Not possible measurement result')
        assert res[0] + res[1] == 100, 'Not possible measurements result'
        assert abs(res[0] - 50) < 15, 'Not fair distribution of results'

        for i in xrange(10):
            q = (Ket(5) + Ket(6)).normalize()
            q.measure()
            if q != Ket(5) and q != Ket(6):
                self.fail('Not possible measurement result')

        q0 = QRegister([ones(8) / sqrt(8)])
        q0.measure()
        assert q0 in [Ket(n, 3) for n in xrange(8)]

        q = (0.9 + 0.6j) * Ket(1, 2) + (0.7 - .1j) * Ket(2,2)
        q.normalize()
        q.measure()

    def testMeasureSome(self):
        q0 = QRegister([ones(8) / sqrt(8)])
        print q0

        q0 = QRegister([ones(8) / sqrt(8)])
        print q0.measure(0)

        q0 = QRegister([ones(8) / sqrt(8)])
        print q0.measure(2, 1)
        print q0
        print q0.dirac()

        q = ket0 ** (s2 * ket0 + s2 * ket1).normalize() ** ket1
        assert q.measure(1) in (Ket(0), Ket(1))
        assert q in (Ket(1, 3), Ket(3, 3))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(QRegisterTestCase))
    suite.addTest(unittest.makeSuite(QubitTestCase))
    suite.addTest(unittest.makeSuite(QclibTestCase))
    unittest.TextTestRunner(verbosity = 2).run(suite)

