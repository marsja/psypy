# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 14:32:14 2015

@author: erik
"""

from psychopy import visual, core  # import some libraries from PsychoPy

#create a window
mywin = visual.Window([800,600], monitor="testMonitor", units="deg")

#create some stimuli
grating = visual.GratingStim(win=mywin, units='cm', mask="circle", size=1.45, pos=[0,0], sf=0)
fixation = visual.TextStim(win=mywin, text='x', pos=[0.0,0.0], color='black', height=2.2, alignHoriz='center', alignVert='center')

#draw the stimuli and update the window
grating.draw()
fixation.draw()
mywin.update()

#pause, so you get a chance to see it!
core.wait(5.0)
core.quit()