#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Sat Sep  2 12:40:43 2017

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

#data_roll[i]=my_float1       
#print("roll: {:.4f}".format(my_float1) )

import serial
import struct
import time
import matplotlib.pyplot as plt
import numpy as np

size=450
data_roll =np.zeros(size)
data_pitch=np.zeros(size)

try:
	ser = serial.Serial('/dev/ttyUSB0',115200)       # open serial port
	print("Using port" + ser.name)                   # check which port was really used

	i=0
	line=ser.readline()

	while i<size:   
		my_float1=ser.read(4)
		line = ser.readline()

		my_float2=ser.read(4)
		line = ser.readline()
		try:
			my_float1 = struct.unpack('<f', my_float1)
			my_float2 = struct.unpack('<f', my_float2)
		except:
			# I/O Error, or junk data
			my_float1 = 0.0
			my_float2 = 0.0

		print(my_float1[0],my_float2[0])
		data_roll[i]  = my_float1[0]
		data_pitch[i] = my_float2[0]
		i=i+1

finally:
	print("Finished receiving")
	time.sleep( 1 )
	print("Closing the port correctly")
	ser.close()                                      # close port

	plt.plot( list(range(size)) ,data_roll)
	plt.plot( list(range(size)) ,data_pitch)
	plt.show()




