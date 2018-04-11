# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 10:30:34 2018

@author: Juan Antonio Barragán Noguera
@email: jabarragann@unal.edu.co

"""

import numpy as np
import matplotlib.pyplot as plt 


#Generar senal con ruido
numS = 30000
n = np.arange(numS)
deltaT=0.001
f=0.1
signal = 1*np.sin(2*np.pi*f*n*deltaT)*np.sin(2*np.pi*2*f*n*deltaT)+1.5
noise = np.random.normal(0,0.2,numS)
sig = signal
signal = signal + noise


#Kalman - Yk+1 = Xk * alpha + Yk * (1 - alpha)
y2 = np.zeros(numS)
alpha = 0.03

for i in range(1,numS):
    y2[i] = ( signal[i-1]*alpha + (1-alpha)*y2[i-1] )

fig,ax=plt.subplots(2)

ax[0].plot(n,sig)
ax[0].set_ylim((0,3))
ax[0].grid()
ax[1].plot(n,signal)
ax[1].plot(n,y2)
ax[1].set_ylim((0,3))
ax[1].grid()
 