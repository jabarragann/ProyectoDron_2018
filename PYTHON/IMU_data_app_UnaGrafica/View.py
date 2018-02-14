# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 21:19:24 2018

@author: Juan Antonio Barragán Noguera
@email: jabarragann@unal.edu.co

"""

import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class View():
    def __init__(self, master):
        
        #Frames
        self.figureFrame = Tk.Frame(master)
        self.sidePanelFrame = Tk.Frame(master)
            
        self.figureFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
        self.sidePanelFrame.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
    
        #Initilize plots
        self.initPlots()
        
        #Figure Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.figureFrame)
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.canvas.show()
        
        #SidePanel Buttons
        self.startButton = Tk.Button(self.sidePanelFrame,text="start",width=15)
        self.startButton.pack(side="top",fill=Tk.BOTH)
        
        self.stopButton = Tk.Button(self.sidePanelFrame,text="stop")
        self.stopButton.pack(side="top",fill=Tk.BOTH)
        
        self.clearButton = Tk.Button(self.sidePanelFrame, text="Clear")
        self.clearButton.pack(side="top",fill=Tk.BOTH)
        
        self.exitButton = Tk.Button(self.sidePanelFrame,text="Exit")
        self.exitButton.pack(side="top",fill=Tk.BOTH)
        
        self.buttonsDict={"start":self.startButton,"stop":self.stopButton,
                          "clear":self.clearButton,"exit":self.exitButton}
        
    def initPlots(self):
        #Matplotlib figures
        plt.ioff()
        self.fig, self.axes = plt.subplots(2,2,gridspec_kw={"width_ratios":[12,1]},figsize=(11, 6), dpi=110 )
        self.ax0=self.axes[0,0]
        self.ax1=self.axes[1,0]
        self.axes[0,1].axis('off')
        self.axes[1,1].axis('off')
        
        self.axesDict={"ax0": self.ax0,"ax1": self.ax1,}
        
        self.initAx(self.ax0,"Time(u)","Acceleration")
        self.initAx(self.ax1,"Time(u)","Angular Vel")
        
        #Init acceleration Line2D 
        self.accX, = self.ax0.plot([], [], color='red',animated=True,label="accelerometer_x")
        self.accY, = self.ax0.plot([], [], color='blue',animated=True,label="accelerometer_y")
        self.accZ, = self.ax0.plot([], [], color='green',animated=True,label="accelerometer_z")
        
        #Init gyroscope Line2D
        self.gyrX, = self.ax1.plot([], [], color='orange',animated=True,label="gyroscope_x")
        self.gyrY, = self.ax1.plot([], [], color='black',animated=True,label="gyroscope_y")
        self.gyrZ, = self.ax1.plot([], [], color='purple',animated=True,label="gyroscope_z")
        
        self.artistDict={"accX": self.accX,"accY": self.accY,"accZ": self.accZ,
                         "gyrX": self.gyrX,"gyrY": self.gyrY,"gyrZ": self.gyrZ,}
        
        #Set Legend
        h0,l0=self.ax0.get_legend_handles_labels()
        h1,l1=self.ax1.get_legend_handles_labels()
        self.axes[0,1].legend(h0,l0, borderaxespad=0,bbox_to_anchor=(1.6, 0.6))
        self.axes[1,1].legend(h1,l1, borderaxespad=0,bbox_to_anchor=(1.12, 0.6))
        
    def initAx (self,ax,xLabel,yLabel):
        ax.set_xlabel(xLabel)
        ax.set_ylabel(yLabel)
        ax.grid()
    
