#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE
class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'


class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 10  # n
        self.data_bits = 6  # k
        self.parity_bits = 4  # r

        # Predefined non-systematic generator matrix G'
        gns = [[1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
               [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
               [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
               [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
               [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(gns)
        self.h = self.__derive_h(self.g)

    def __convert_to_g(self, gns: List):
        """
        Converts a non-systematic generator matrix into a systematic

        Args:
            gns (List): Non-systematic generator matrix
        Returns:
            list: Converted systematic generator matrix
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        for i in range(10):
            gns[2][i] = gns[2][i] ^ gns[0][i]
            gns[4][i] = gns[4][i] ^ gns[0][i]
            gns[5][i] = gns[5][i] ^ gns[0][i]  # Subtracting row 1 from: row 3, row 5, row 6
        for i in range(10):
            gns[0][i] = gns[0][i] ^ gns[1][i]
            gns[2][i] = gns[2][i] ^ gns[1][i]
            gns[5][i] = gns[5][i] ^ gns[1][i]  # Subtracting row 2 from: row 1, row 3, row 6
        for i in range(10):
            gns[0][i] = gns[0][i] ^ gns[2][i]
            gns[4][i] = gns[4][i] ^ gns[2][i]
            gns[5][i] = gns[5][i] ^ gns[2][i]  # Subtracting row 3 from: row 1, row 5, row 6
        for i in range(10):
            gns[0][i] = gns[0][i] ^ gns[3][i]
            gns[2][i] = gns[2][i] ^ gns[3][i]  # Subtracting row 4 from: row 1, row 3
        for i in range(10):
            gns[1][i] = gns[1][i] ^ gns[4][i]
            gns[2][i] = gns[2][i] ^ gns[4][i]  # Subtracting row 5 from: row 2, row 3
        for i in range(10):
            gns[0][i] = gns[0][i] ^ gns[5][i]
            gns[1][i] = gns[1][i] ^ gns[5][i]
            gns[4][i] = gns[4][i] ^ gns[5][i]  # Subtracting row 6 from: row 1, row 2, row 5

        list = []
        list = gns
        return list

    def __derive_h(self, g: List):

        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:
        """
        g_matrix = [[1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
                    [0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
                    [0, 0, 0, 1, 0, 0, 1, 1, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 1, 0, 1, 0, 1]]
        parity_matrix = [g_matrix[0][6:],
                         g_matrix[1][6:],
                         g_matrix[2][6:],
                         g_matrix[3][6:],
                         g_matrix[4][6:],
                         g_matrix[5][6:]]

        transpose_matrix = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        for i in range(6):
            for j in range(4):
                transpose_matrix[j][i] = parity_matrix[i][j]
        list = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]

        for i in range(4):
            for j in range(6):
                list[i][j] = transpose_matrix[i][j]

        return list

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """
        global tuple
        test = []
        G_Matrix = (
        (1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1), (0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1), (0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0),
        (0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1), (0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0),
        (0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1))
        for i in range(11):
            total = 0
            x = 0
            for j in range(6):
                total = source_word[j] * G_Matrix[j][i]
                if (j == 0):
                    x = total
                else:
                    x = x ^ total
            test.append(x)
        test_2 = tuple(test)
        print("Encoded word is", test_2)
        return test_2

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """
        parity_1 = 0
        for i in range(11):
            parity_1 = parity_1 ^ encoded_word[i]
        print("overall parity is", parity_1)
        res_1 = []
        msw = []
        for i in range(10):
            res_1.append(encoded_word[i])
            if (i < 6):
                msw.append(encoded_word[i])
        print(res_1)
        print(msw)
        synd = []
        H_Matrix = [[1, 0, 0, 1],
                    [0, 0, 1, 1],
                    [1, 1, 1, 0],
                    [1, 1, 0, 0],
                    [0, 1, 1, 1],
                    [0, 1, 0, 1],
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]]
        for i in range(4):
            total = 0
            x = 0
            for j in range(10):
                total = res_1[j] * H_Matrix[j][i]
                if (j == 0):
                    x = total
                else:
                    x = x ^ total
            synd.append(x)
        print("The syndrome is ",synd)

        synd_total = 0
        for i in range(4):
            synd_total = synd_total + synd[i]
        if (parity_1 == 0):
            if (synd_total == 0):
                print("Zero errors")
                print("Decoded word is ", msw)
                Union = (*msw,)
                print(Union)
                return Union, HCResult.VALID
        if (parity_1 == 1):
            if (synd_total == 0):
                print("Error is in the parity bit")
                print("Decoded word is", msw)
                Union = (*msw,)
                print(Union)
                return Union, HCResult.CORRECTED
        if (parity_1 == 1):
            if (synd_total != 0):
                print("Single error")
                for i in range(10):
                    if (synd == H_Matrix[i]):
                        print("Error is in position =", i)
                        if (i < 6):
                            if (msw[i] == 0):
                                msw[i] = 1
                            else:
                                msw[i] = 0
                print("Corrected decoded word is", msw)
                Union = (*msw,)
                print(Union)
                return Union, HCResult.CORRECTED
        if (parity_1 == 0):
            if (synd_total != 0):
                print("Multiple errors")
                print("Decoded word is ", msw)
                Union = (*msw,)
                return Union, HCResult.UNCORRECTABLE
