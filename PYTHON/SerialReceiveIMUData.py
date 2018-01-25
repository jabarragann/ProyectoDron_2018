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

size=550
data_gyrox  =np.zeros(size)
data_gyroy  =np.zeros(size)
data_gyroz  =np.zeros(size)
data_accelx =np.zeros(size)
data_accely =np.zeros(size)
data_accelz =np.zeros(size)

IMU_data=np.zeros((size,6))

try:
	ser = serial.Serial('/dev/ttyUSB0',115200)       # open serial port
	print("Using port" + ser.name)                   # check which port was really used

	i=0
	line=ser.readline()

	while i<size:
		for j in range(6):   
			my_float1=ser.read(4)
						
			try:
				my_float1 = struct.unpack('<f', my_float1)
			except:
				# I/O Error, or junk data
				my_float1 = 0.0
			
			#print(my_float1[0], end=" ")
			
			IMU_data[i][j]=my_float1[0]
		
		print("ax:{:2.3f} ay:{:2.3f} az:{:2.3f}".format(IMU_data[i][0],IMU_data[i][1],IMU_data[i][2]))
		print("gx:{:2.3f} gy:{:2.3f} gz:{:2.3f}".format(IMU_data[i][3],IMU_data[i][4],IMU_data[i][5]))

		i=i+1
		line = ser.readline()
		

finally:
	print("Finished receiving")
	time.sleep( 1 )
	print("Closing the port correctly")
	ser.close()                                      # close port

	fig,axes=plt.subplots(2)
	axes[0].plot( list(range(size)) ,IMU_data[:,0])
	axes[0].plot( list(range(size)) ,IMU_data[:,1])
	axes[0].plot( list(range(size)) ,IMU_data[:,2])
	
	axes[1].plot( list(range(size)) ,IMU_data[:,3])
	axes[1].plot( list(range(size)) ,IMU_data[:,4])
	axes[1].plot( list(range(size)) ,IMU_data[:,5])
	

	dataFile=open("roll_data1.csv","w")
	
	dataFile.write("ax,ay,az,gx,gy,gz\n")
	for i in range(size):
		dataFile.write("{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}\n".format(IMU_data[i][0],IMU_data[i][1],IMU_data[i][2],IMU_data[i][3],IMU_data[i][4],IMU_data[i][5]))

	plt.show()


	




