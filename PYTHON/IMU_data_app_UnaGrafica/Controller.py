# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 21:52:58 2018

@author: Juan Antonio Barragán Noguera
@email: jabarragann@unal.edu.co

"""
import Model
import View
import tkinter as Tk
import numpy as np
import time

import matplotlib.animation as animation

import serial
import struct

t3=0 

class Controller():
    def __init__(self,serialInfo):
        
        self.serialInfo=serialInfo
        self.dataSize=100000
        self.root = Tk.Tk()
        self.model=Model.Model(self.dataSize)
        self.view=View.View(self.root)
        
        #Bind Buttons to methods
        self.view.buttonsDict["clear"].bind("<Button-1>",self.clear)
        self.view.buttonsDict["exit"].bind("<Button-1>",self.closeApp)
        self.view.buttonsDict["stop"].bind("<Button-1>",self.stop)
        self.view.buttonsDict["start"].bind("<Button-1>",self.start)
        
        #Init Animation
        self.ani=SubplotAnimation(self.view.fig,self.view.axesDict,self.view.artistDict,self.model,self.serialInfo)
        self.animationController = self.ani.animationController
        
  
    def run(self):
        self.root.title("Tkinter MVC example")
        self.root.deiconify()
        self.root.mainloop()
         
    
    #Buttons Binding Methods
    def start(self,event):
        
        if not self.ani.ser.isOpen():
             self.ani.ser = serial.Serial(self.serialInfo['name'],self.serialInfo['baudRate']) 
            
        self.animationController.event_source.start()
    
    def stop(self,event):
        
        if self.ani.ser.isOpen():
             self.ani.ser.close() 
             
        self.animationController.event_source.stop()
        
        
    def clear(self,event):
        pass
      
    def closeApp(self,event):
        self.ani.ser.close()
        self.root.quit()
        self.root.destroy()
        
  
    def my_plot(self,event):
        self.model.calculate()
        
        self.view.ax0.clear()
        self.view.ax0.grid()
        self.view.ax0.plot(np.arange(200),self.model.cos_data,marker='*',linestyle='None',color='orange')
        
        self.view.fig.canvas.draw()
    
class SubplotAnimation(animation.TimedAnimation):
    
    def __init__(self,fig,axesDict,artistDict,model,serialInfo):
        
        self.serialInfo=serialInfo
        self.width=350
        self.model=model
        self.fig = fig
        self.ax0 = axesDict['ax0']
        self.ax1 = axesDict['ax1']
    
        #Init acceleration Lines 
        self.accLine1 = artistDict['accX'] 
        self.accLine2 = artistDict['accY']
        self.accLine3 = artistDict['accZ']
    
        #Init gyroscope Lines
        self.gyrLine1 = artistDict['gyrX']
        self.gyrLine2 = artistDict['gyrY']
        self.gyrLine3 = artistDict['gyrZ']
        
        #self.lines=[self.accLine1,self.accLine2,self.accLine3,self.gyrLine1,self.gyrLine2, self.gyrLine3]
        self.lines=[self.accLine2,self.accLine3]
        
        #test data
        self.t = np.arange(400)
        self.x = np.cos(0.2 * np.pi * self.t / 10.)
        self.y = np.sin(0.2 * np.pi * self.t / 10.)
        self.z = 10 * self.t

        
        self.ax0.set_xlim(-1, self.width)
        self.ax0.set_ylim(-2, 2)

        self.ax1.set_xlim(-1, self.width)
        self.ax1.set_ylim(-2, 2)
        
        
        self.ser = serial.Serial(self.serialInfo['name'],self.serialInfo['baudRate'])  # open serial port
        #self.ser.readline()
        
        self.animationController=animation.FuncAnimation(self.fig, self._draw_frame, 
                                         init_func=self._init_draw,interval=1,
                                         frames=np.arange(self.model.dataSize),blit=True)
        
    def _draw_frame(self, framedata):
        i = self.model.index
        
        #print("Buffer size: ", self.ser.inWaiting())
        
		#Wait until 6 floats has been received. The sixth floats correspond to:
		#acc_x, acc_y, acc_z, gyr_x, gyr_y and gyr_z.
        if self.ser.inWaiting() >= 12*4:
            
            global t3
            t1=time.time()
            print("Elapsed time:" ,(t1-t3)*1000,"Buffer size: ", self.ser.inWaiting())
            #print("Buffer size:{:4d} ; Index: {:4d} ".format(self.ser.inWaiting(),self.model.index))
            
            #Dynamically change x limits
            if i > 0.9*self.width:
                xlim=self.ax0.get_xlim()
                increase=self.model.time[i]-self.model.time[i-1]
                self.ax0.set_xlim(xlim[0]+increase,xlim[1]+increase)
                
                xlim=self.ax1.get_xlim()
                increase=self.model.time[i]-self.model.time[i-1]
                self.ax1.set_xlim(xlim[0]+increase,xlim[1]+increase)
            
            #Read serial Data and fill IMU data matrix
            for k in range(6):    
                s = self.ser.read(4)
                try:
                    my_float1 = struct.unpack('<f', s)
                except Exception as e:
                    # I/O Error, or junk data
                    my_float1 = 0.0
                    print(e)
                
                self.model.IMU_data[i,k]=my_float1[0]
            
            #Data that will not be plotted
            for k in range(6):    
                s = self.ser.read(4)
                try:
                    my_float1 = struct.unpack('<f', s)
                except Exception as e:
                    # I/O Error, or junk data
                    my_float1 = 0.0
                    print(e)
                
            t2=time.time()
            #print("Elapsed time:",i,":" ,(t2-t1)*1000)
            
            
            #Calculate attitude
            ''''
            self.model.calculateAttitudeGyro(self.model.IMU_data[i,3],\
                              self.model.IMU_data[i,4],\
                              self.model.IMU_data[i,5],\
                              i,10E-3)
            
            self.model.calculateAttitudeAccel(self.model.IMU_data[i,0],\
                              self.model.IMU_data[i,1],\
                              self.model.IMU_data[i,2],\
                              i)
            
            self.model.calculateComplementaryFilter(0.3,i)
            '''
            
            #Calcuate attitude Method 2
            self.model.calculateComplementaryFilter2(i, self.model.IMU_data[i,0], \
                                                       self.model.IMU_data[i,1], \
                                                       self.model.IMU_data[i,2], \
                                                       self.model.IMU_data[i,3], \
                                                       self.model.IMU_data[i,4], \
                                                       self.model.IMU_data[i,5],\
                                                       l=0.9)
			
            '''		
			  #Plot Accelerometer Values
            self.accLine1.set_data(self.model.time[:i], self.model.IMU_data[:i,0])
            self.accLine2.set_data(self.model.time[:i], self.model.IMU_data[:i,1])
            self.accLine3.set_data(self.model.time[:i], self.model.IMU_data[:i,2])
            
            '''
            
            '''
            #Plot Euler angles (gyro)
            self.accLine1.set_data(self.model.time[:i], self.model.yawn_gyro_deg[:i])
            self.accLine2.set_data(self.model.time[:i], self.model.pitch_gyro_deg[:i])
            self.accLine3.set_data(self.model.time[:i], self.model.roll_gyro_deg[:i])
            '''
            
            '''
            #Plot Euler angles (accelerometer)
            self.accLine1.set_data(self.model.time[:i], self.model.yawn_gyro_deg[:i])
            self.accLine2.set_data(self.model.time[:i], self.model.pitch_accel_deg[:i])
            self.accLine3.set_data(self.model.time[:i], self.model.roll_accel_deg[:i])
            '''
			 
            
            #Plot Euler angles complementary filter
            self.accLine1.set_data(self.model.time[:i], self.model.yawn[:i])
            self.accLine2.set_data(self.model.time[:i], self.model.pitch[:i])
            self.accLine3.set_data(self.model.time[:i], self.model.roll[:i])
			 
              
			#Plot Gyroscope values
            self.gyrLine1.set_data(self.model.time[:i], self.model.IMU_data[:i,3])
            self.gyrLine2.set_data(self.model.time[:i], self.model.IMU_data[:i,4])
            self.gyrLine3.set_data(self.model.time[:i], self.model.IMU_data[:i,5])
            
			#self.lines is an iterable that has the lines that are going to be dynamically updated in the graphs 
            #self.lines=[self.accLine1,self.accLine2,self.accLine3,self.gyrLine1,self.gyrLine2, self.gyrLine3]
            self.lines=[self.accLine2,self.accLine3]
            self._drawn_artists = self.lines
            
            
            #self.ser.readline()
            self.model.index+=1
            t3=time.time()
            #print("Elapsed time:",i,":" ,(t3-t2)*1000)
            
        return self.lines
        
        
    def _test_animation(self, framedata):
        i = framedata
        
        if self.t[i]> 0.95*self.width:
            xlim=self.ax0.get_xlim()
            increase=self.t[i]-self.t[i-1]
            self.ax0.set_xlim(xlim[0]+increase,xlim[1]+increase)
            
            xlim=self.ax1.get_xlim()
            increase=self.t[i]-self.t[i-1]
            self.ax1.set_xlim(xlim[0]+increase,xlim[1]+increase)
        

        self.accLine1.set_data(self.t[:i], self.y[:i])
        self.accLine2.set_data(self.t[:i], 0.5*np.ones( (i,1) ) )
        self.accLine3.set_data(self.t[:i], 0*np.ones( (i,1) ) )
        
        self.gyrLine1.set_data(self.t[:i], self.x[:i])
        self.gyrLine2.set_data(self.t[:i], 0.5*np.ones( (i,1) ) )
        self.gyrLine3.set_data(self.t[:i], 0*np.ones( (i,1) )   )
        
        self._drawn_artists = self.lines
        
    def new_frame_seq(self):
        return iter(range(self.t.size))

    def _init_draw(self):
        self.ax0.set_xlim(-1, self.width)
        self.ax0.set_ylim(-100,100)

        self.ax1.set_xlim(-1, self.width)
        self.ax1.set_ylim(-220, 220)

        for l in self.lines:
            l.set_data([], [])
            
        return self.lines
