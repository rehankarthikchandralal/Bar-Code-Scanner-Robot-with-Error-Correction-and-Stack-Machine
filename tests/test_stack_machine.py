#!/usr/bin/env python3

import unittest
from unittest.mock import patch, call
from stack_machine import StackMachine, SMState
from ctypes import c_ubyte

class TestStackMachine(unittest.TestCase):
    def setUp (self):
        self.sm = StackMachine()

    def tearDown (self):
        del self.sm

    def test_instance(self):
        """ Essential: Test class instantiation """
        self.assertEqual(self.sm.getState(), SMState.IDLE)
        self.assertEqual(self.sm.top(), None)

    @patch("stack_machine.StackMachine.utPrint")
    def test_top(self, mock_print):
        """ Test Method: top() """
        # Check for "None"
        self.assertEqual(self.sm.top(), None)

        # Check for "String"
        self.sm.do((1, 0, 0, 1, 0, 0))
        self.assertEqual(self.sm.top(), "A")

        # Check for "tuple(1 byte long)"
        self.sm.do((0, 0, 0, 0, 1, 0))
        self.assertEqual(self.sm.top(), (0, 0, 0, 0, 0, 0, 1, 0))

    @patch("stack_machine.StackMachine.utPrint")
    def test_do(self, mock_print):
        """ Test Method: do() """
        Instructs = [(0, 0, 1, 0, 1, 0),
                     (0, 1, 0, 0, 0, 1),
                     (0, 1, 0, 0, 0, 1),
                     (0, 1, 0, 1, 1, 0),
                     (0, 1, 1, 1, 1, 1),
                     (0, 0, 0, 1, 0, 0),
                     (0, 1, 1, 0, 1, 1),
                     (0, 0, 0, 1, 0, 0),
                     (0, 1, 1, 0, 0, 1),
                     (0, 0, 0, 1, 1, 0),
                     (0, 1, 1, 0, 0, 0),
                     (1, 0, 0, 0, 1, 0),
                     (1, 1, 0, 1, 1, 0),
                     (1, 0, 1, 0, 0, 0),
                     (1, 1, 0, 1, 0, 1),
                     (0, 0, 0, 1, 0, 1),
                     (1, 0, 0, 0, 0, 1),
                     (0, 1, 0, 0, 0, 0)]

        for i in range(len(Instructs) - 1):  # Execute until SPEAK Instruction and assert output
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual(mock_print.mock_calls, [call("TEXT = ", "RES 64")])

        # Execute STP Instruction and assert output
        self.assertEqual(self.sm.do(Instructs[len(Instructs) - 1]), SMState.STOPPED)

    def test_Dup(self):
        """ Test Method: Dup() """
        Instructs = [(0, 0, 1, 0, 1, 0),
                     (0, 1, 0, 0, 0, 1)]

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual(self.sm.stack[0].value, self.sm.stack[1].value)

    def test_Del(self):
        """ Test Method: Del() """
        Instructs = [(0, 0, 1, 0, 1, 0),
                     (0, 1, 0, 0, 1, 0)]

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual(self.sm.top(), None)

    def test_Swp(self):
        """ Test Method: Swp() """
        Instructs = [(0, 0, 1, 0, 1, 0),  # push 10
                     (0, 0, 0, 0, 1, 0)]  # push 2

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [10, 2])
        # Perform Swap
        self.sm.do((0, 1, 0, 0, 1, 1))
        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [2, 10])

    def test_Add(self):
        """ Test Method: Add() """
        Instructs = [(0, 0, 1, 0, 1, 0),  # push 10
                     (1, 0, 0, 1, 0, 0)]  # push A

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1]], [10, "A"])

        # Perform Add and test for Operand Mismatch
        self.assertEqual(self.sm.do((0, 1, 0, 1, 0, 0)), SMState.ERROR)

    def test_Sub(self):
        """ Test Method: Sub() """
        Instructs = [(0, 0, 0, 0, 1, 0),  # push 2
                     (0, 0, 1, 0, 1, 0)]  # push 10

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [2, 10])

        # Perform Sub and also test for Overflow
        self.sm.do((0, 1, 0, 1, 0, 1))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [256 - 8, True])

    def test_Mul(self):
        """ Test Method: Mul() """
        Instructs = [(0, 0, 0, 0, 1, 0),  # push 2
                     (0, 0, 1, 0, 1, 0)]  # push 10

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [2, 10])

        # Perform Mul and also test for Overflow
        self.sm.do((0, 1, 0, 1, 1, 0))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [20, False])

    def test_Div(self):
        """ Test Method: Mul() """
        Instructs = [(0, 0, 0, 0, 1, 0),  # push 2
                     (0, 0, 0, 0, 0, 0)]  # push 10

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [2, 0])

        # Perform Div and also test for Division by zero
        self.assertEqual(self.sm.do((0, 1, 0, 1, 1, 1)), SMState.ERROR)

    def test_Exp(self):
        """ Test Method: Exp() """
        Instructs = [(0, 0, 0, 0, 1, 0),  # push 2
                     (0, 0, 1, 0, 1, 0)]  # push 10

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [2, 10])

        # Perform Exp and also test for Overflow
        self.sm.do((0, 1, 1, 0, 0, 0))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [0, True])

    def test_Mod(self):
        """ Test Method: Mod() """
        Instructs = [(0, 0, 1, 0, 1, 0),  # push 10
                     (0, 0, 0, 1, 1, 1)]  # push 7

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [10, 7])

        # Perform Exp and also test for Overflow
        self.sm.do((0, 1, 1, 0, 0, 1))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [3, False])

    def test_Shl(self):
        """ Test Method: Shl() """
        Instructs = [(0, 0, 1, 0, 1, 0),  # push 10
                     (0, 0, 0, 1, 1, 1)]  # push 7

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [10, 7])

        # Perform Shl and also test for Overflow
        self.sm.do((0, 1, 1, 0, 1, 0))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [0, True])

    def test_Shr(self):
        """ Test Method: Shr() """
        Instructs = [(0, 0, 1, 0, 1, 0),  # push 10
                     (0, 0, 0, 1, 1, 1)]  # push 7

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [10, 7])

        # Perform Shr and also test for Overflow
        self.sm.do((0, 1, 1, 0, 1, 1))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [0, False])

    def test_Hex(self):
        """ Test Method: Hex() """
        Instructs = [(0, 0, 1, 0, 1, 0),  # push 10
                     (0, 0, 0, 1, 1, 1)]  # push 7

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [10, 7])

        # Perform Hex and also test for Operand Mismatch (10 cant be HEX value)
        self.assertEqual(self.sm.do((0, 1, 1, 1, 0, 0)), SMState.ERROR)
        # Perform HEX for AA
        self.sm.do((1, 0, 0, 1, 0, 0))
        self.sm.do((1, 0, 0, 1, 0, 0))
        self.sm.do((0, 1, 1, 1, 0, 0))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [170, False])

    def test_Ieq(self):
        """ Test Method: Ieq() """
        Instructs = [(0, 0, 1, 0, 1, 0),  # push 10
                     (0, 0, 0, 1, 1, 1)]  # push 7

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [10, 7])

        # Perform Ieq and also test for Overflow
        self.sm.do((0, 1, 1, 1, 0, 1))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [0, False])

    def test_Not(self):
        """ Test Method: Not() """
        Instructs = [(0, 0, 1, 0, 1, 0)]  # push 10

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value], [10])

        # Perform Not and also test for Overflow
        self.sm.do((0, 1, 1, 1, 1, 0))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [5, False])

    def test_Xor(self):
        """ Test Method: Xor() """
        Instructs = [(0, 0, 1, 0, 1, 0),  # push 10
                     (0, 0, 0, 1, 1, 1)]  # push 7

        for i in range(len(Instructs)):
            if self.sm.getState() in (SMState.RUNNING, SMState.IDLE):
                self.sm.do(Instructs[i])

        self.assertEqual([self.sm.stack[0].value, self.sm.stack[1].value], [10, 7])

        # Perform Ieq and also test for Overflow
        self.sm.do((0, 1, 1, 1, 1, 1))
        self.assertEqual([self.sm.stack[0].value, self.sm.overflow], [13, False])


if __name__ == '__main__':
    unittest.main()

