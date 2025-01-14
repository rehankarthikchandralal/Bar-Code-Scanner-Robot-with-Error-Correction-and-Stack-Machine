#!/usr/bin/env python3

import io
import unittest.mock
from hamming_code import *
from stack_machine import *


class TestRobot(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_example(self, mock_stdout):
        r =Robot()
        tr=StackMachine()
        h=HammingCode()
        self.assertEqual((0, 0, 0, 0, 0, 1, 1, 0), tr.top(), "Correct")
        

if __name__ == '__main__':
    unittest.main()
