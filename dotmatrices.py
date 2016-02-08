# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 22:05:30 2015

@author: erik
"""

# Import what you need
import numpy
from psychopy import visual, event, monitors,core

# Some variables and a window

mon = monitors.Monitor('My screen', width=37.5, distance=57)
mon.setSizePix((1280,1024))
win = visual.Window(size=(800, 800),color='lightgray', units='cm', monitor=mon)
# Create a matrix with 0's and 1's. Here a 3x3 identity-matrix 
dotMatrix = numpy.eye(5)

def dotPos():
        rectByRow = 5
        rectByCol = 5
        size = 14 / rectByRow
        positions = []
        for row in range(rectByCol):
            for col in range(rectByCol):
                #Row three should bee y = 0 middle row!
                if col == 0:x=-5.6 
                elif col == 2:x=0
                elif col == 1:x=-2.8 
                elif col == 3:x=2.8
                elif col == 4:x=5.6
                if row == 0:y=-5.6
                elif row == 2:y=0
                elif row == 1:y=-2.8
                elif row == 3:y=2.8
                elif row == 4:y=5.6  

                pos = (x,y)
                
                positions.append(pos)
        return positions

position = dotPos()   
print(position)     
#visual.Rect(win, height=14, width=14,pos=(0,0), fillColor=(-2,-1,-1), lineColor=None).draw()
#for rect in position:
#    print rect
#    visual.Rect(win, height=2.8, width=2.8,pos=rect, fillColor=(1,1,1), lineColor=None).draw()

for dot in position:
    visual.Circle(win, radius=1, fillColor='black', lineColor='black', pos=dot).draw()
stim1 = visual.BufferImageStim(win)
win.flip()
core.wait(5)
win.close()