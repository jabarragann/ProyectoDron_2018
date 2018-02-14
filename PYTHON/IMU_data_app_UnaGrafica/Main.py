# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 22:02:55 2018

@author: Juan Antonio Barragán Noguera
@email: jabarragann@unal.edu.co

"""

import Controller

if __name__ == '__main__':
    
    serialInfo={'name':'COM4','baudRate':57600}
    c = Controller.Controller(serialInfo)
    c.run()