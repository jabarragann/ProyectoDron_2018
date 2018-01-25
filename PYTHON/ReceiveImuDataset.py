#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Sep  2 17:21:34 2017

@author: Juan Antonio Barragán Noguera
@email : jabarragann@unal.edu.co

"""


'''
Important Note:

The float must be send in reverse order from the microcontroller so that struct.unpack can
correctly re build the float variable. Also the float variable must be send as Char ( 2 Bytes )

pseudo example code that must be in the microcontroller:
    
float pi=12.141422; ----> 0x41424344
char *fPointer = (char *) &pi;
chprintf((BaseChannel *)&SD1, "%c%c%c%c\n",fPointer[0],fPointer[1],fPointer[2],fPointer[3]);

'''

import serial
import struct
import time

try:
    ser = serial.Serial('/dev/ttyUSB0',115200)       # open serial port
    print("Using port" + ser.name)                   # check which port was really used
    
    i=0
    line=ser.readline()

    while i<6:   
        my_float1=ser.read(4)
        try:
            my_float1 = struct.unpack('<f', my_float1)
            print(my_float1)
        except:
            # I/O Error, or junk data
            my_float1 = 0.0
        
        i=i+1

finally:
    print("Finished receiving")
    time.sleep( 1 )
    print("Closing the port correctly")
    ser.close()                                      # close port




