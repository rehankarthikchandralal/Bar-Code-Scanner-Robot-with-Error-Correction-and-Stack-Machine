#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time


class Robot:
    """
    -- TEMPLATE --
    This class provides logic for moving the sensor and scrolling the bar code cards
    """

    def sensor_step(self):
        """
        Moves the sensor one step to read the next bar code value
        """
        # implementation
        pass
        m = ev3.LargeMotor("outA")
        m.reset()
        m.speed_sp = 77
        m.command="run-forever"
        time.sleep(1.75)
        m.time_sp=2
        m.stop_action="brake"
        m.run_timed()
        m.stop()
        time.sleep(1)



    

    def sensor_reset(self):
        """
        Resets the sensor position
        """
        # implementation
        pass
        m = ev3.LargeMotor("outA")
        m.reset()
        m.speed_sp = -385
        m.command="run-forever"
        time.sleep(3.86)
        m.time_sp=2
        m.stop_action="brake"
        m.run_timed()
        m.stop()
        time.sleep(1)

       

    def scroll_step(self):
        """
        Moves the bar code card to the next line.
        """
        # implementation
        pass
        m = ev3.LargeMotor('outB')
        m.reset()
        m.speed_sp = 140
        m.command="run-forever"
        time.sleep(0.5)
        m.stop()
        time.sleep(1)



    def read_value(self) -> int:
        """
        Reads a single value, converts it and returns the binary expression
        :return: int
        """
        # implementation
        cs=ev3.ColorSensor()
        cs.mode='RGB-RAW'
        cs.bin_data("hhh")
        b=()
        b=cs.bin_data("hhh")
        print(cs.bin_data("hhh"))
        tup_white1=(290,470,220)
        tup_white2=(260,400,160)
        if b[2]<= 220 and b[2]>=160:
            print("White")
            return 0
        tup_red1=(275,280,130)
        tup_red2=(230,230,85)
        if b[0]<=275 and b[0]>=230:
            if b[1]<=280 and b[1]>=230:
                if b[2]<=130 and b[2]>=85:
                    print("Red")
                    return 5
        tup_black1=(180,360,120)
        tup_black2=(100,230,60)
        if b[0]<= 180 and b[0]>=100:
            print("Black")
            return 1
       

               
        

       
