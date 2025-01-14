#!/usr/bin/env python3

from hamming_code import HammingCode
from stack_machine import StackMachine
from robot import *
import ev3dev.ev3 as ev3


def run():
    # the execution of all code shall be started from within this function
    r=Robot()
    tr=StackMachine()
    h=HammingCode()
    counter=0
    while counter<5:                                #Loop for constantly calibrating with red
        while r.read_value()==5:
            print("Red detected ",r.read_value())
            time.sleep(8)
            i=0
            flag=False
            list_1=[]
            tup_1=()
            for i in range(11):                      #Reads a line 
                r.sensor_step()
                t=r.read_value()
                if t==None:
                    flag=True
                list_1.append(t)
                print ("Read bit is",t)
                print(i)
            time.sleep(2)
            r.sensor_reset()                       #Resets sensor to initial position
            if flag==True:                                        #Re reading line in case of WRONG value detected
                print("Re reading line because of None ")
                time.sleep(15)
                list_1=[]
                for i in range(11):
                    r.sensor_step()
                    t=r.read_value()
                    list_1.append(t)
                    print ("Read bit is",t)
                    print(i)
                time.sleep(2)
                r.sensor_reset()  
            tup_1=tuple(list_1)
            print(list_1)
            print(tup_1)
            ev3.Sound.speak("eleven bit input is").wait()             #Printing 11 bit encoded word read my barcode sensor
            ev3.Sound.speak(tup_1).wait()
            out_tuple=()
            out_tuple=h.decode(tup_1)
            print(out_tuple)
            if out_tuple[1] == 'ERROR':               #Re reading line in case of Uncorrectable code
                print("Re reading line because of Uncorrectable code ")
                time.sleep(2)
                list_1=[]
                for i in range(11):
                    r.sensor_step()
                    t=r.read_value()
                    list_1.append(t)
                    print ("Read bit is",t)
                    print(i)
                time.sleep(2)
                r.sensor_reset()  
            print(" The Opcode is",out_tuple)                       #Printing 6 bit output of decode from HammingCode
            ev3.Sound.speak("six bit output is").wait()
            ev3.Sound.speak(out_tuple[0]).wait()
            time.sleep(3)
            tr.do(out_tuple[0])                                    #Executing StackMACHINE
            print("THE TOP ELEMENT OF STACK IS")                   #Printing top element of Stack
            print(tr.top())
            time.sleep(2)
            print("Execution finished for One line")               #Execution finished for One line
            time.sleep(4)
            r.scroll_step()                                        #Scroller motor works to move to next line
        time.sleep(5)
        continue

        
    
 
    
    
    
    
    
    
   



   


    
    



   






if __name__ == '__main__':
    run()
