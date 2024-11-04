import unittest

from hamming_code import *       #importing subclasses

m = HammingCode()   #assigning class to variable
class TestHammingCode(unittest.TestCase):
    def test_instance(self):
        """ Essential: Test class instantiation """
        m=HammingCode()

    def test_decode_valid(self):
        """ Essential: Test method decode() with VALID input """
        result1 = ((1, 0, 1, 1, 0, 1),HCResult.VALID)
        result2 = m.decode((1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1))
        self.assertEqual(result1, result2, "Correct")

    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """
        result1 = ((0, 1, 1, 0, 1, 1), HCResult.CORRECTED)
        result2 = m.decode((0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0))
        self.assertEqual(result1, result2, "Correct")

        result1 = ((0, 0, 0, 0, 0, 0), HCResult.CORRECTED)
        result2 = m.decode((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1))
        self.assertEqual(result1, result2, "Correct")

        result1 = ((1, 1, 1, 1, 1, 0), HCResult.CORRECTED)
        result2 = m.decode((1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1))
        self.assertEqual(result1, result2, "Correct")

        result1 = ((0, 0, 0, 0, 0, 0), HCResult.CORRECTED)
        result2 = m.decode((0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(result1, result2, "Correct")

    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """
        result1 = ((1, 0, 0, 1, 0, 0), HCResult.UNCORRECTABLE)
        result2 = m.decode((1,0,0,1,0,0,0,0,0,0,0))
        self.assertEqual(result1, result2, "Correct")


    def test_encode(self):                      #testing encode function
        """ Essential: Test method encode() """
        result3 = (0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0)
        result4 =m.encode((0, 1, 1, 0, 1, 1))
        self.assertEqual(result3, result4, "Correct")

        result3 = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        result4 = m.encode((0, 0, 0, 0, 0, 0))
        self.assertEqual(result3, result4, "Correct")

        result3 = (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1)
        result4 = m.encode((1, 0, 1, 1, 0, 1))
        self.assertEqual(result3, result4, "Correct")

        result3 = (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)
        result4 = m.encode((1,1,1,1,1,0))
        self.assertEqual(result3, result4, "Correct")


if __name__ == '__main__':
    unittest.main()








