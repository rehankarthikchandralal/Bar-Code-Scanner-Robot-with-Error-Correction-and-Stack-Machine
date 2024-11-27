#!/usr/bin/env python3

from enum import IntEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class SMState(IntEnum):
    """
    Return codes for the stack machine
    """
    IDLE = 2
    RUNNING = 1
    STOPPED = 0
    ERROR = -1
    EMPTY = -2           # Stack is Empty


class StackMachine:
    """
    -- TEMPLATE --
    Implements the 8-bit stack machine according to the specification
    """
    def __init__(self):
        """
        Initializes the class StackMachine with all values necessary.
        """
        self.overflow = False
        self.stack = []
        self.tp = len(self.stack) - 1               # Top of stack pointer
        self.StackState = SMState.IDLE              # Initialize stack with Idle state

        # Hashtable for instructions/character values
        self.Operation = { "010000" : "STP",        # Signals end of execution. Does not consider or even remove an element from stack | No change | 0/0
                           "010001" : "DUP",        # Duplicates the last operand | No change | 1/2
                           "010010" : "DEL",        # Removes the last operand | No change | 1/0
                           "010011" : "SWP",        # Swaps the last two operands | No change | 2/2
                           "010100" : "ADD",        # Adds Top to Top-1 | True if addition resulted in a carry out of the most-significant bit, False otherwise | 2/1
                           "010101" : "SUB",        # Subtracts Top from Top-1 | True if subtraction resulted in a borrow out of the most-significant bit, False otherwise | 2/1
                           "010110" : "MUL",        # Multiplies the last two operands | True if product doesn’t fit into data type, False otherwise | 2/1
                           "010111" : "DIV",        # Divides Top-1 by Top | False | 2/1
                           "011000" : "EXP",        # Calculates Top-1 ** Top | True if product doesn’t fit into data type, False otherwise | 2/1
                           "011001" : "MOD",        # Calculates Top-1 modulo Top | False | 2/1
                           "011010" : "SHL",        # Shifts Top-1 by Top places to the left | True if a 1 is shifted out of the operand, False otherwise | 2/1
                           "011011" : "SHR",        # Shifts Top-1 by Top places to the right | False | 2/1
                           "011100" : "HEX",        # Converts a sequence of hexadecimal into integer (Top to Top-1) | False | 2/1
                           "011101" : "IEQ",        # Returns 1 if Top-1 is equal to Top, otherwise 0 | False | 2/1
                           "011110" : "NOT",        # Forms the ones' complement of Top | False | 1/1
                           "011111" : "XOR",        # Performs the logical XOR operation on Top and Top-1 bit by bit | False | 2/1
                           "100001" : "SPEAK",      # Execute Text-to-Speech on decoded character list - Pop first item from stack (number, n) - Now, pop n items from the stack and store them for TTS processing - Execute TTS
                           "100000" : "NOP",        # No Operation
                           "100011" : "NOP",        # No Operation
                           "111110" : "NOP",        # No Operation 
                           "111111" : "NOP" }       # No Operation

        self.Character = { "100010" : " ",          # Push "SPACE" to stack
                           "100100" : "A",          # Push "A" to stack
                           "100101" : "B",          # Push "B" to stack
                           "100110" : "C",          # Push "C" to stack
                           "100111" : "D",          # Push "D" to stack
                           "101000" : "E",          # Push "E" to stack
                           "101001" : "F",          # Push "F" to stack
                           "101010" : "G",          # Push "G" to stack
                           "101011" : "H",          # Push "H" to stack
                           "101100" : "I",          # Push "I" to stack
                           "101101" : "J",          # Push "J" to stack
                           "101110" : "K",          # Push "K" to stack
                           "101111" : "L",          # Push "L" to stack 
                           "110000" : "M",          # Push "M" to stack 
                           "110001" : "N",          # Push "N" to stack 
                           "110010" : "O",          # Push "O" to stack 
                           "110011" : "P",          # Push "P" to stack 
                           "110100" : "Q",          # Push "Q" to stack 
                           "110101" : "R",          # Push "R" to stack 
                           "110110" : "S",          # Push "S" to stack 
                           "110111" : "T",          # Push "T" to stack 
                           "111000" : "U",          # Push "U" to stack 
                           "111001" : "V",          # Push "V" to stack     
                           "111010" : "W",          # Push "W" to stack 
                           "111011" : "X",          # Push "X" to stack 
                           "111100" : "Y",          # Push "Y" to stack 
                           "111101" : "Z", }        # Push "Z" to stack 

        # Dictionary to dynamically call functions
        self.DynFunc = { "STP" : self.__Stp,
                         "DUP" : self.__Dup,
                         "DEL" : self.__Del,
                         "SWP" : self.__Swp,
                         "ADD" : self.__Add,
                         "SUB" : self.__Sub,
                         "MUL" : self.__Mul,
                         "DIV" : self.__Div,
                         "EXP" : self.__Exp,
                         "MOD" : self.__Mod,
                         "SHL" : self.__Shl,
                         "SHR" : self.__Shr,
                         "HEX" : self.__Hex,
                         "IEQ" : self.__Ieq,
                         "NOT" : self.__Not,
                         "XOR" : self.__Xor,
                         "SPEAK" : self.__Speak }

    def utPrint (self, *args):
        """
        Print function used to print Unit-Tests outputs
        Param : *args
        """
        string = ""
        for i in range(len(args)):
            string += "".join(str(args[i]) if not isinstance(args[i], str) else args[i])
        print (string)

    def __pop (self):
        """
        Returns the top most element of the stack and removes it.
        Returns None in case of underflow
        """
        if (self.stack):
            self.tp -= 1
            x = self.stack.pop()
            if (isinstance(x, c_ubyte)):
                return x.value
            else:
                return x
        else:
            #print ("Stack Underflow")
            return SMState.EMPTY

    def __push (self, elem):
        """
        Pushes new element as c_ubyte into stack top and increaments the top pointer
        """
        if (isinstance(elem, str)):
            self.stack.append(elem)
        else:
            self.stack.append(c_ubyte(int(elem)))

        self.tp += 1

    def __Stp (self):
        """
        End the execution of stack machine
        """
        # Do things / clean up if necessary before stopping operations
        # Currently does nothing
        return SMState.STOPPED

    def __Dup (self):
        """
        Duplicate the top of stack
        """
        x = self.__pop()
        if (x != SMState.EMPTY):
            self.__push(x)
            self.__push(x)
            return SMState.RUNNING
        else:
            return SMState.EMPTY

    def __Del (self):
        """
        Removes the top element
        """
        x = self.__pop()
        if (x != SMState.EMPTY):
            return SMState.RUNNING
        else:
            return SMState.EMPTY

    def __Swp (self):
        """
        Swaps top and top-1
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()
        if (y == SMState.EMPTY):
            # Restore x to stack
            self.__push(x)
            return SMState.EMPTY

        self.__push(x)
        self.__push(y)
        return SMState.RUNNING

    def __Add (self):
        """
        Adds top and top-1
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()
        if (y == SMState.EMPTY):
            # Restore x to stack
            self.__push(x)
            return SMState.EMPTY

        # Check if operands are of the same type
        if (not isinstance(x, type(y))):
            #print ("Operand type mismatch")
            return SMState.ERROR

        # Set overflow flag to true if carry of MSB happens
        if (x+y > 255):
            self.overflow = True

        self.__push(x+y)
        return SMState.RUNNING

    def __Sub (self):
        """
        Subtracts top from top-1
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()

        # Check if operands are of the same type
        if (not isinstance(x, int) or not isinstance(y, int)):
            #print ("Operand type mismatch")
            return SMState.ERROR

        # Set overflow flag to true if borrow of MSB happens
        if (y-x < 0):
            self.overflow = True

        self.__push(y-x)
        return SMState.RUNNING

    def __Mul (self):
        """
        Multiply top and top-1
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()

        # Check if operands are of the same type
        if (not isinstance(x, int) or not isinstance(y, int)):
            #print ("Operand type mismatch")
            return SMState.ERROR

        # Set overflow flag to true if product doesnt fit in c_ubyte
        if (x*y > 255):
            self.overflow = True

        self.__push(x*y)
        return SMState.RUNNING

    def __Div (self):
        """
        Divide top-1 by top
        """
        x = self.__pop()
        print ("x =", x)
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        print ("x =", x)
        y = self.__pop()
        print ("y =", y)
        if (y == SMState.EMPTY):
            # Restore x to stack
            self.__push(x)
            return SMState.EMPTY
        print ("y =", y)

        # Check if operands are of the same type
        if (not isinstance(x, int) or not isinstance(y, int)):
            #print ("Operand type mismatch")
            return SMState.ERROR

        # Check for division by zero
        if (x == 0):
            #print ("Invalid Division")
            # Return elements to stack in same order
            self.__push(y)
            self.__push(x)
            return SMState.ERROR
        
        self.__push(y/x)
        return SMState.RUNNING

    def __Exp (self):
        """
        Compute top-1 ** top
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()

        # Check if operands are of the same type
        if (not isinstance(x, int) or not isinstance(y, int)):
            #print ("Operand type mismatch")
            return SMState.ERROR

        # Set overflow flag to true if product doesnt fit in c_ubyte
        if (y**x > 255):
            self.overflow = True

        self.__push(y**x)
        return SMState.RUNNING
    
    def __Mod (self):
        """
        Calculate mod of top-1 on top
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()

        # Check if operands are of the same type
        if (not isinstance(x, int) or not isinstance(y, int)):
            #print ("Operand type mismatch")
            return SMState.ERROR

        if (x == 0):
            #print ("Invalid Division")
            # Return elements to stack in same order
            self.__push(y)
            self.__push(x)
            return SMState.ERROR

        self.__push(y%x)
        return SMState.RUNNING

    def __Shl (self):
        """
        Shifts top-1 by top to the left
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()

        # Check if operands are of the same type
        if (not isinstance(x, int) or not isinstance(y, int)):
            #print ("Operand type mismatch")
            return SMState.ERROR
        
        # Check for overflow
        if (y<<x > 255):
            self.overflow = True
        self.__push(y<<x)
        return SMState.RUNNING

    def __Shr (self):
        """
        Shifts top-1 by top to the right
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()

        # Check if operands are of the same type
        if (not isinstance(x, int) or not isinstance(y, int)):
            #print ("Operand type mismatch")
            return SMState.ERROR

        self.__push(y>>x)
        return SMState.RUNNING

    def __Hex (self):
        """
        Converts a sequence of hexadecimal into integer (top to top-1)
        """
        valid = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]   # Possible valid values for x and y

        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()

        # Check if x and y are within 0-9 and A-F
        x = str(x)
        y = str(y)
        if (x not in valid or y not in valid):
            #print ("Conversion to Hex not possible")
            return SMState.ERROR

        self.__push(int(x+y, 16))
        return SMState.RUNNING

    def __Ieq (self):
        """
        Return 1 if top == top-1, 0 otherwise
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()
        if (y == SMState.EMPTY):
            # Restore x to stack
            self.__push(x)
            return SMState.EMPTY

        if (y == x):
            self.__push(1)
        else:
            self.__push(0)
        return SMState.RUNNING

    def __Not (self):
        """
        Compute 1's complement of the element
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        
        if (not isinstance(x, int)):
            #print ("Element is not an Int, cannot complement")
            return SMState.ERROR

        string1 = bin(x)
        string2 ="0b"
        for i in range(2,len(string1)):
            string2 += "".join(str(int(string1[i])^1))
        self.__push(int(string2, 2))
        return SMState.RUNNING

    def __Xor (self):
        """
        Perform bitwise XOR on top and top-1
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY
        y = self.__pop()
        if (y == SMState.EMPTY):
            # Restore x to stack
            self.__push(x)
            return SMState.EMPTY

        if (not isinstance(x, int) or not isinstance(y, int)):
            #print ("Elements are not Int, cannot XOR")
            return SMState.ERROR
            
        string1 = format(x, "08b")
        string2 = format(y, "08b")
        string3 = "".join([str(int(x)^int(y)) for x,y in zip(string1, string2)])
        self.__push(int(string3, 2))
        return SMState.RUNNING

    def __Speak (self):
        """
        Emulate TTS by printing to console
        """
        x = self.__pop()
        if (x == SMState.EMPTY):
            return SMState.EMPTY

        string = ""
        # Pop x elements and add them to string
        for i in range(x):
            y = self.__pop()
            if (y == SMState.EMPTY):
                if (string):
                    self.utPrint ("TEXT (Incomplete) = ", string)
                else:
                    # Restore x to stack
                    self.__push(x)
                return SMState.EMPTY
            string += "".join(str(y))
        self.utPrint ("TEXT = ", string)
        return SMState.RUNNING

    def do(self, code_word):
        """
        Processes the entered code word by either executing the instruction or pushing the operand on the stack.
        :param code_word: 6-tuple
        :returns: SMState
        """
        code_word = list(code_word)

        self.StackState = self.__compute(code_word)
        
        # Check for state and handle appropriately
        if (self.StackState == SMState.EMPTY):
            #self.utPrint ("Stopping Stack Machine, state = ", self.StackState)
            self.StackState = SMState.ERROR

        return self.StackState

    def top(self):
        """
        Returns the top element of the stack.
        :returns: 8-tuple or None
        """
        ret_val = None
        if (self.tp >= 0):
            if (isinstance(self.stack[self.tp], c_ubyte)):
                ret_val = tuple (map(lambda x: int(x), format(self.stack[self.tp].value, "08b")))
            else:
                ret_val = self.stack[self.tp]
        #self.utPrint ("Top = ", ret_val)
        return ret_val
    
    def __compute (self, code_word):
        """
        Perform the respective computation determined by the received code_word and return the computation result and state.
        returns: SMState
        """
        code_word = list(code_word)
        string = ""
        char = False                # Set flag is operation is a character

        # Convert the code_word into a string for easy computation
        for i in range (len(code_word)):
            string += "".join(str(code_word[i]))

        # In case of an operand, push it onto the stack
        if (string[0] == '0' and string[1] == '0'):
            self.__push(int(string, 2))
            self.overflow = False
            return SMState.RUNNING

        # Find the corresponding operation from the Hashtable
        opr = self.Operation.get(string)
        if (opr == None):
            opr = self.Character.get(string)
            if (opr == None):
                #print ("Invalid Instruction")
                return SMState.ERROR
            else:
                char = True

        if (opr == "NOP"):
            # Do nothing
            return SMState.RUNNING

        elif (char):
            self.__push(opr)
            return SMState.RUNNING

        else:
            # Dynamically call the respective execution functions
            func = self.DynFunc[opr]
            state = func()
            return state

    def dispStack (self):
        """
        Print stack to console for debugging
        """
        if (self.stack):
            print ("Stack (rightmost elem is top) =", self.stack, "Overflow =", self.overflow)
        else:
            print ("Stack EMPTY")

    def getState (self):
        """
        Returns the current state of the stack
        """
        return self.StackState
