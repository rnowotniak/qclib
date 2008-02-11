#!/usr/bin/python
# -*- coding: iso8859-2 -*-
#


import unittest

from qclib import *

class QRegister(unittest.TestCase):

    def setUp(self):
        pass

    def testNormalize(self):
        self.assertTrue(True)
        pass

    def testKets(self):
        pass

    def testQubits(self):
        pass

    def testTensor(self):
        pass

    def testGates(self):
        pass



if __name__ == '__main__':
    suite = unittest.makeSuite(QRegister)
    unittest.TextTestRunner(verbosity = 2).run(suite)

