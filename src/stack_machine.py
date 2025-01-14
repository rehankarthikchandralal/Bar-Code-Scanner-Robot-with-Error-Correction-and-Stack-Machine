#!/usr/bin/env python3

from enum import IntEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte
from robot import *
import ev3dev.ev3 as ev3


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class SMState(IntEnum):
    """
    Return codes for the stack machine
    """
    RUNNING = 1
    STOPPED = 0
    ERROR = -1


class StackMachine:
    """
    Implements the 8-bit stack machine according to the specification
    """

    def __init__(self) -> None:
        """
        Initializes the class StackMachine with all values necessary.
        """
        self.overflow = False
        self.stack = []
        self.SMState=1
        # Hashtable for instructions/character values
        self.Instruction = {"010000": "STP",  # Signals end of execution
                            "010001": "DUP",  # Duplicates the last operand
                            "010010": "DEL",  # Removes the last operand
                            "010011": "SWP",  # Swaps the last two operands
                            "010100": "ADD",  # Adds Top to Top-1
                            "010101": "SUB",  # Subtracts Top from Top-1
                            "010110": "MUL",  # Multiplies the last two operands
                            "010111": "DIV",  # Divides Top-1 by Top
                            "011000": "EXP",  # Calculates Top-1 ** Top
                            "011001": "MOD",  # Calculates Top-1 modulo Top
                            "011010": "SHL",  # Shifts Top-1 by Top places to the left
                            "011011": "SHR",  # Shifts Top-1 by Top places to the right
                            "011100": "HEX",  # Hexadecimal to decimal
                            "011110": "NOT",  # Forms the ones' complement of Top
                            "011111": "XOR",  # Performs the logical XOR operation on Top and Top-1 bit by bit
                            "100001": "SPEAK",# Execute Text-to-Speech
                            "100000": "NOP",  # No Operation
                            "100011": "NOP",  # No Operation
                            "111110": "NOP",  # No Operation
                            "111111": "NOP"}  # No Operation

        self.Character = {"100010": " ",  # Push "SPACE" to stack
                          "100100": "A",  # Push "A" to stack
                          "100101": "B",  # Push "B" to stack
                          "100110": "C",  # Push "C" to stack
                          "100111": "D",  # Push "D" to stack
                          "101000": "E",  # Push "E" to stack
                          "101001": "F",  # Push "F" to stack
                          "101010": "G",  # Push "G" to stack
                          "101011": "H",  # Push "H" to stack
                          "101100": "I",  # Push "I" to stack
                          "101101": "J",  # Push "J" to stack
                          "101110": "K",  # Push "K" to stack
                          "101111": "L",  # Push "L" to stack
                          "110000": "M",  # Push "M" to stack
                          "110001": "N",  # Push "N" to stack
                          "110010": "O",  # Push "O" to stack
                          "110011": "P",  # Push "P" to stack
                          "110100": "Q",  # Push "Q" to stack
                          "110101": "R",  # Push "R" to stack
                          "110110": "S",  # Push "S" to stack
                          "110111": "T",  # Push "T" to stack
                          "111000": "U",  # Push "U" to stack
                          "111001": "V",  # Push "V" to stack
                          "111010": "W",  # Push "W" to stack
                          "111011": "X",  # Push "X" to stack
                          "111100": "Y",  # Push "Y" to stack
                          "111101": "Z", }  # Push "Z" to stack

    def do(self, code_word: Tuple[int, ...]) -> SMState:
        """
        Processes the entered code word by either executing the instruction or pushing the operand on the stack.

        Args:
            code_word (tuple): Command for the stack machine to execute
        Returns:
            SMState: Current state of the stack machine
        """
        # REPLACE "pass" WITH YOUR IMPLEMENTATION

        length = len(self.stack)
        print("Length of stack", length)
        string = ""
        overflow = False
        def execute(str1):
                if (str1 == "010011"):  # Swap Instruction
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction Swap").wait()
                    print("SWAP")
                    x = self.stack.pop()
                    y = self.stack.pop()
                    self.stack.append(x)
                    self.stack.append(y)
                    print(x)
                    print(y)
                    return 1
                elif (str1 == "010001"):  # Duplicate Instruction
                    x = self.stack.pop()
                    self.stack.append(x)
                    self.stack.append(x)
                    ev3.Sound.speak("Instruction Duplicate").wait()
                    print("DUPLICATE")
                    return 1

                elif (str1 == "010000"):  # Stop Instruction
                    ev3.Sound.speak("Instruction Stop").wait()
                    print("STOP")
                    print("End of Execution")
                    print("Final Stack is", self.stack)
                    print("SMSSTAte")
                    return 0
                    quit()

                elif (str1 == "010010"):  # Delete Instruction
                    ev3.Sound.speak("Instruction Delete").wait()
                    print("DELETE")
                    self.stack.pop()
                    return 1
                elif (str1 == "010100"):  # Add Instruction
                    ev3.Sound.speak("Instruction Add").wait()
                    print("ADD")
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    x = self.stack.pop()
                    y = self.stack.pop()
                    z = x + y
                    if (z > 255):
                        overflow = True
                        print("There is overflow")
                        print("overflow = ", overflow)
                    else:
                        overflow = False
                        self.stack.append(z)
                    return 1
                elif (str1 == "010101"):  # Subtract instruction
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction Subtract").wait()
                    print("SUBTRACT")
                    x = self.stack.pop()
                    y = self.stack.pop()
                    z = y - x
                    if (z < 0):
                        overflow = True
                        print("There is overflow")
                        print("overflow = ", overflow)
                    else:
                        overflow = False
                        self.stack.append(z)
                    return 1
                elif (str1 == "010110"):  # Multiplication instruction
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction Multiply").wait()
                    print("MULTIPLICATION")
                    x = self.stack.pop()
                    y = self.stack.pop()
                    z = x * y
                    if (z > 255):
                        overflow = True
                        print("There is overflow")
                        print("overflow = ", overflow)
                    else:
                        overflow = False
                        self.stack.append(z)
                    return 1
                elif (str1 == "010111"):  # Division instruction
                    if (length < 2):
                        print("Not enough operands")
                        print("SMState ERROR")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction Division").wait()
                    print("DIVISION")
                    x = self.stack.pop()
                    if (x == 0):
                        print("ERROR Division by 0 not possible")
                        print("SMState ERROR")
                        return -1
                        quit()
                    y = self.stack.pop()
                    z = y // x
                    self.stack.append(z)
                    return 1
                elif (str1 == "011000"):  # Exponent instruction
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction Exponent").wait()
                    print("EXPONENT")
                    x = self.stack.pop()
                    y = self.stack.pop()
                    z = y ** x
                    if (z > 255):
                        overflow = True
                        print("There is overflow")
                        print("overflow = ", overflow)
                    else:
                        overflow = False
                        self.stack.append(z)
                    return 1
                elif (str1 == "011001"):  # Modulo instruction
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction Modulus").wait()
                    print("MODULUS")
                    x = self.stack.pop()
                    y = self.stack.pop()
                    z = y % x
                    self.stack.append(z)
                    return 1
                elif (str1 == "011010"):  # Shift to Left Instruction
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction Shift to left").wait()
                    print("SHIFT TO LEFT")
                    x = self.stack.pop()
                    y = self.stack.pop()
                    z = y << x
                    if (z > 255):
                        overflow = True
                        print("There is overflow")
                        print("overflow = ", overflow)
                    else:
                        overflow = False
                        self.stack.append(z)
                    print(z)
                    return 1
                elif (str1 == "011011"):  # Shift to Right Instruction
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction Shift to right").wait()
                    print("SHIFT TO RIGHT")
                    x = self.stack.pop()
                    y = self.stack.pop()
                    z = y >> x
                    print(z)
                    self.stack.append(z)
                    return 1
                elif (str1 == "011100"):  # Hexadecimal Instruction
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction Hexadecimal").wait()
                    print("HEXADECIMAL")
                    x = self.stack.pop()
                    y = self.stack.pop()
                    z = 0
                    tot = 0
                    is_Int = True
                    try:
                        int(x)
                    except:
                        is_Int = False
                    if is_Int:
                        tot = 16 * x
                    else:
                        if (x == 'A'):
                            z = 10
                        elif (x == 'B'):
                            z = 11
                        elif (x == 'C'):
                            z = 12
                        elif (x == 'D'):
                            z = 13
                        elif (x == 'E'):
                            z = 14
                        elif (x == 'F'):
                            z = 15
                        tot = tot + 16 * z
                    is_Int_1 = True
                    try:
                        int(y)
                    except:
                        is_Int_1 = False
                    if is_Int_1:
                        tot = tot + y
                    else:
                        if (y == 'A'):
                            z = 10
                        elif (y == 'B'):
                            z = 11
                        elif (y == 'C'):
                            z = 12
                        elif (y == 'D'):
                            z = 13
                        elif (y == 'E'):
                            z = 14
                        elif (y == 'F'):
                            z = 15
                        tot = tot + z
                    print(tot)
                    self.stack.append(tot)
                    return 1


                elif (str1 == "011101"):  # Factorial instruction
                    ev3.Sound.speak("Instruction Factorial").wait()
                    print("FACTORIAL")
                    x = self.stack.pop()
                    z = 1
                    j = 1
                    for i in range(x):
                        z = z * j
                        j += 1
                    print(z)
                    if (z > 255):
                        overflow = True
                        print("There is overflow")
                        print("overflow = ", overflow)
                    else:
                        overflow = False
                        self.stack.append(z)
                    return 1
                elif (str1 == "011110"):  # 1s Complement instruction
                    ev3.Sound.speak("Instruction ones complement").wait()
                    print("NOT 1S COMPLEMENT")
                    x = self.stack.pop()
                    st2 = "0b"
                    binary = bin(x)
                    positive_binary = format(x, 'b')
                    tp = tuple(positive_binary)
                    i = 1
                    b = []
                    n = x
                    while (n > 0):
                        d = n % 2
                        b.append(d)
                        n = n // 2
                        i += 1
                    while (i != 5):
                        b.append(0)
                        i += 1
                    b.reverse()
                    print("Binary Tuple is: ", b)  # returning integer as binary tuple

                    k = 4
                    while (k != 8):
                        st2 += "".join(str(0))
                        print(st2)
                        k += 1


                    for i in range(4):
                        st2 += "".join(str(int(b[i]) ^ 1))
                        print(st2)


                    self.stack.append(int(st2,2))
                    return 1
                elif (str1 == "011111"):  # XOR instruction
                    if (length < 2):
                        print("Not enough operands")
                        return -1
                        quit()
                    ev3.Sound.speak("Instruction XOR").wait()
                    print("XOR")
                    x = self.stack.pop()
                    y = self.stack.pop()
                    st1 = bin(x)
                    st2 = bin(y)
                    k = int(st1, 2) ^ int(st2, 2)
                    print("Bitwise Xor is")
                    print('{0:b}'.format(k))
                    self.stack.append(k)
                    return 1

        for i in range(len(code_word)):
                string += "".join(str(code_word[i]))
        print(string)
        if (code_word[0] == 0):
                if (code_word[1] == 0):
                    print("Operand")
                    k = int(string, 2)
                    print(k)
                    self.stack.append(k)
                    print("The stack is")
                    print(self.stack)
                    return 1

                elif (code_word[1] == 1):
                    print("Instruction")
                    k=execute(string)
                    print("The stack is")
                    print(self.stack)
                    print("SMState value is",k)
                    return(k)
        elif (code_word[0] == 1):
                print("Character")
                if (string == "100100"):
                    self.stack.append("A")  # Push "A" to stack
                elif (string == "100101"):
                    self.stack.append("B")  # Push "B" to stack
                elif (string == "100110"):
                    self.stack.append("C")  # Push "C" to stack
                elif (string == "100111"):
                    self.stack.append("D")  # Push "D" to stack
                elif (string == "101000"):
                    self.stack.append("E")  # Push "E" to stack
                elif (string == "101001"):
                    self.stack.append("F")  # Push "F" to stack
                elif (string == "101010"):
                    self.stack.append("G")  # Push "G" to stack
                elif (string == "101011"):
                    self.stack.append("H")  # Push "H" to stack
                elif (string == "101100"):
                    self.stack.append("I")  # Push "I" to stack
                elif (string == "101101"):
                    self.stack.append("J")  # Push "J" to stack
                elif (string == "101110"):
                    self.stack.append("K")  # Push "K" to stack
                elif (string == "101111"):
                    self.stack.append("L")  # Push "L" to stack
                elif (string == "110000"):
                    self.stack.append("M")  # Push "M" to stack
                elif (string == "110001"):
                    self.stack.append("N")  # Push "N" to stack
                elif (string == "110010"):
                    self.stack.append("O")  # Push "O" to stack
                elif (string == "110011"):
                    self.stack.append("P")  # Push "P" to stack
                elif (string == "110100"):
                    self.stack.append("Q")  # Push "Q" to stack
                elif (string == "110101"):
                    self.stack.append("R")  # Push "R" to stack
                elif (string == "110110"):
                    self.stack.append("S")  # Push "S" to stack
                elif (string == "110111"):
                    self.stack.append("T")  # Push "T" to stack
                elif (string == "111000"):
                    self.stack.append("U")  # Push "U" to stack
                elif (string == "111001"):
                    self.stack.append("V")  # Push "V" to stack
                elif (string == "111010"):
                        self.stack.append("W")  # Push "W" to stack
                elif (string == "111011"):
                    self.stack.append("X")  # Push "X" to stack
                elif (string == "111100"):
                    self.stack.append("Y")  # Push "Y" to stack
                elif (string == "111101"):  # Push "Z" to stack
                    self.stack.append("Z")
                elif (string == "100010"):  # Push " " to stack(SPACE)
                    self.stack.append("  ")
                elif (string == "100000"):  # NOP
                    print("NOP")
                    return 1
                elif (string == "111110"):  # NOP
                    print("NOP")
                    return 1
                elif (string == "111111"):  # NOP
                    print("NOP")
                    return 1
                elif (string == "100011"):  # NOP
                    print("NOP")
                    return 1
                elif (string == "100001"):  # SPEAK Command
                    print("SPEAK Command")
                    k = self.stack.pop()
                    speakstack = []
                    print('The number of elements removed from stack is',k,)
                    for i in range(k):
                        speakstack.append(self.stack.pop())
                    print("SPEAK OUTPUT", speakstack)
                    ev3.Sound.speak(speakstack).wait()
                    print(self.stack)
                    return 1

                print("The stack is")
                print(self.stack)
                return 1

        print("The stack is")
        print(self.stack)


    def top(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:
        """
        Returns the top element of the stack.

        Returns:
            union: Can be tuple, str or None
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        if (self.stack == []):  # checking for empty stack
            print("NONE")
            print("EMPTY STACK")
            union = None
            return union
        top = self.stack.pop()  # popping out last element of stack
        print(top)
        is_Int = True  # checking the data type of top element
        try:
            int(top)
        except:
            is_Int = False
        if is_Int:
            if (top < 0):  # Checking for integer range error
                print("RANGE ERROR:The Integer Value is out of 8 bit range")
            elif (top > 256):
                print("RANGE ERROR:The Integer Value is out of 8 bit range")
            else:
                ev3.Sound.speak("Top element is").wait()
                ev3.Sound.speak(top).wait()
                print("the top element is", top)
                binary = bin(top)
                positive_binary = format(top, 'b')
                tp = tuple(positive_binary)
                i = 1
                b = []
                n = top
                while (n > 0):
                    d = n % 2
                    b.append(d)
                    n = n // 2
                    i += 1
                while (i != 9):
                    b.append(0)
                    i += 1
                b.reverse()
                print("Binary Tuple is: ", b)  # returning integer as binary tuple
                self.stack.append(top)
                union =tuple(b)
                return union
        else:
            print("Entered thing is not an Integer")
            print("the top element is", top)  # printing character top element
            self.stack.append(top)
            union = top
            return union  # pushing top element back to stack
        print("The stack is")
        print(self.stack)  # printing stack






