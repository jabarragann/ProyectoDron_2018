# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 21:13:40 2018

@author: Juan Antonio Barragán Noguera
@email: jabarragann@unal.edu.co

"""

import numpy as np
from numpy import sin, cos, tan, arcsin, arctan

class Model():
 
    def __init__(self,dataSize):
        
        self.time=np.arange(dataSize)
        self.dataSize=dataSize
        
        self.IMU_data=np.zeros((dataSize,6))
        
        #Gyro based euler angles
        self.yawn_gyro=np.zeros((dataSize,1))
        self.pitch_gyro=np.zeros((dataSize,1))
        self.roll_gyro=np.zeros((dataSize,1))
        
        self.yawn_gyro_deg=np.zeros((dataSize,1))
        self.pitch_gyro_deg=np.zeros((dataSize,1))
        self.roll_gyro_deg=np.zeros((dataSize,1))
       
        #Accelerometer based euler angles
        self.pitch_accel=np.zeros((dataSize,1))
        self.roll_accel=np.zeros((dataSize,1))
        
        self.pitch_accel_deg=np.zeros((dataSize,1))
        self.roll_accel_deg=np.zeros((dataSize,1))
        
        #Final Values
        self.yawn=np.zeros((dataSize,1))
        self.pitch=np.zeros((dataSize,1))
        self.roll=np.zeros((dataSize,1))
        
        
        self.index=1
  
  
    def getSetdata(self,row,data):
       self.IMU_data[row,:]=data
       
    
    def calculateAttitudeGyro(self,gyr_x,gyr_y,gyr_z,index,samplingTime):
        
        #convert to rad/sec
        gyr_x=gyr_x * np.pi/180
        gyr_y=gyr_y * np.pi/180
        gyr_z=gyr_z * np.pi/180
        
        derivate= np.zeros((3,1))
        
        derivate[0]= gyr_x+gyr_y*sin(self.roll_gyro[index-1])*tan(self.pitch_gyro[index-1]) \
                            +gyr_z*cos(self.roll_gyro[index-1])*tan(self.pitch_gyro[index-1])
                            
        derivate[1]= gyr_y*cos(self.roll_gyro[index-1])-gyr_z*sin(self.roll_gyro[index-1])
        
        derivate[2]= gyr_y*sin(self.roll_gyro[index-1])/cos(self.pitch_gyro[index-1])     \
                        +gyr_z*cos(self.roll_gyro[index-1])/cos(self.pitch_gyro[index-1])
                        
        
        self.pitch_gyro[index]=self.pitch_gyro[index-1] +samplingTime*derivate[0]
        self.roll_gyro[index]=self.roll_gyro[index-1] +samplingTime*derivate[1]
        self.yawn_gyro[index]=self.yawn_gyro[index-1] +samplingTime*derivate[2]
        
        
        self.yawn_gyro_deg[index]=self.yawn_gyro[index]*180/np.pi
        self.pitch_gyro_deg[index]=self.pitch_gyro[index]*180/np.pi
        self.roll_gyro_deg[index]=self.roll_gyro[index]*180/np.pi
    
    def calculateAttitudeAccel(self,accel_x,accel_y,accel_z,index):

        t1=accel_x/1.07
        if abs(t1)<1:
            accel_x=t1
        elif accel_x<0:
            accel_x=-1
        else:
            accel_x=1
        
        self.roll_accel[index]=arcsin(accel_x)
        self.pitch_accel[index]=arctan(accel_y/accel_z)
        
        self.pitch_accel_deg[index]=self.pitch_accel[index]*180/np.pi
        self.roll_accel_deg[index]=self.roll_accel[index]*180/np.pi
        
     
    def calculateComplementaryFilter(self,l,index):
        
        self.pitch[index] = self.pitch_gyro_deg[index] + \
            l*(self.pitch_accel_deg[index]-self.pitch_gyro_deg[index])
        
        self.roll[index] = self.roll_gyro_deg[index] + \
            l*(self.roll_accel_deg[index]-self.roll_gyro_deg[index])
            
        self.yawn[index] = 0 
        
        
        
                        