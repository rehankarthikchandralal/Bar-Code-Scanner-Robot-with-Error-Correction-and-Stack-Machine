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
        self.total_bits = 0  # n
        self.data_bits = 0  # k
        self.parity_bits = 0  # r

        # Predefined non-systematic generator matrix G'
        gns = []

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
        gns = [[1, 1, 1, 0, 0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 1, 0, 0, 1, 0, 0], [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
               [0, 0, 0, 1, 0, 0, 1, 1, 0, 0], [1, 1, 0, 1, 0, 0, 0, 1, 1, 0],
               [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]]  # input non-systematic generator matrix
        r1 = [1, 1, 1, 0, 0, 0, 0, 1, 0, 0]
        r2 = [0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
        r3 = [1, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        r4 = [0, 0, 0, 1, 0, 0, 1, 1, 0, 0]
        r5 = [1, 1, 0, 1, 0, 0, 0, 1, 1, 0]
        r6 = [1, 0, 0, 1, 0, 0, 0, 1, 0, 1]
        for i in range(10):  # start of performing row operations for conversion
            r3[i] = r3[i] ^ r1[i]
            r5[i] = r5[i] ^ r1[i]
            r6[i] = r6[i] ^ r1[i]
        for i in range(10):
            r3[i] = r3[i] ^ r2[i]
            r1[i] = r1[i] ^ r2[i]
            r6[i] = r6[i] ^ r2[i]
        for i in range(10):
            r1[i] = r1[i] ^ r3[i]
            r5[i] = r5[i] ^ r3[i]
            r6[i] = r6[i] ^ r3[i]
        for i in range(10):
            r1[i] = r1[i] ^ r4[i]
            r3[i] = r3[i] ^ r4[i]
        for i in range(10):
            r2[i] = r2[i] ^ r5[i]
            r3[i] = r3[i] ^ r5[i]
        for i in range(10):
            r1[i] = r1[i] ^ r6[i]
            r2[i] = r2[i] ^ r6[i]
            r5[i] = r5[i] ^ r6[i]
        list = [[r1], [r2], [r3], [r4], [r5], [r6]]
        print("Systematic Generator Matrix G is", list)  # printing  Systematic  generator matrix G

    def __derive_h(self, g: List):
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        g = [[1, 0, 0, 0, 0, 0, 1, 0, 0, 1], [0, 1, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 1, 0, 0, 0, 1, 1, 1, 0],
             [0, 0, 0, 1, 0, 0, 1, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
             [0, 0, 0, 0, 0, 1, 0, 1, 0, 1]]  # systematic generator matrix
        parity = [[1, 0, 0, 1, ],
                  [0, 0, 1, 1],
                  [1, 1, 1, 0],
                  [1, 1, 0, 0],
                  [0, 1, 1, 1],
                  [0, 1, 0, 1]]
        transposed = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        for i in range(6):
            for j in range(4):
                transposed[j][i] = parity[i][j]  # transposing parity section
        list = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
        for i in range(4):
            for j in range(6):
                list[i][j] = transposed[i][j]  # combining with identity matrix
        print('Systematic Parity check Matrix H is', list)  # printing Systematic parity check matrix H
        return list

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        global tuple
        result = []
        G=()
        G1 = ((1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1), (0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1), (0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0),
              (0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1), (0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0),
              (0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1))
        G=tuple(G1)
        for i in range(11):
            total = 0
            x = 0
            for j in range(6):
                total = source_word[j] * G[j][i]
                if (j == 0):
                    x = total
                else:
                    x = x ^ total
            result.append(x)
        tuple1 = tuple(result)
        print("Encoded word is", tuple1)
        return tuple1

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        overallparity = 0
        for i in range(11):
            overallparity = overallparity ^ encoded_word[i]
        print("overall parity is", overallparity)
        result1 = []
        messageword = []
        for i in range(10):
            result1.append(encoded_word[i])
            if (i < 6):
                messageword.append(encoded_word[i])
        print(result1)
        print(messageword)
        syndrome = []
        Htranspose = [[1, 0, 0, 1], [0, 0, 1, 1], [1, 1, 1, 0], [1, 1, 0, 0], [0, 1, 1, 1], [0, 1, 0, 1], [1, 0, 0, 0],
                      [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        for i in range(4):
            total = 0
            x = 0
            for j in range(10):
                total = result1[j] * Htranspose[j][i]
                if (j == 0):
                    x = total
                else:
                    x = x ^ total
            print(x)
            syndrome.append(x)
        print("Syndrome vector is", syndrome)
        syndrometotal = 0
        for i in range(4):
            syndrometotal = syndrometotal + syndrome[i]
        print("Syndrometotal", syndrometotal)
        if (overallparity == 0):
            if (syndrometotal == 0):
                print("Zero errors")
                print("Decoded word is ", messageword)
                Union = tuple(messageword)
                print(Union)
                return Union,HCResult.VALID
        if (overallparity == 1):
            if (syndrometotal == 0):
                print("Error is in the parity bit")
                print("Decoded word is", messageword)
                Union = tuple(messageword)
                print(Union)
                return Union,HCResult.CORRECTED
        if (overallparity == 1):
            if (syndrometotal != 0):
                print("Single error")
                for i in range(10):
                    if (syndrome == Htranspose[i]):
                        print("Error is in position =", i)
                        if (i < 6):
                            if (messageword[i] == 0):
                                messageword[i] = 1
                            else:
                                messageword[i] = 0
                print("Corrected decoded word is", messageword)
                Union = tuple(messageword)
                print(Union)
                return Union,HCResult.CORRECTED
        if (overallparity == 0):
            if (syndrometotal != 0):
                print("Multiple errors")
                print("Decoded word is ", messageword)
                Union = tuple(messageword)
                print("Uncorrectable errors in ", Union)
                return Union,HCResult.UNCORRECTABLE





