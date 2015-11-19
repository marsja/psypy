# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 20:00:35 2015

@author: erik at marsja dot se, http://www.marsja.se

Adaptation of the local-global task of Miyake et al., (2000)
At least as I have interpreted it from the sparse description in the paper.
Here the keyboard is used to respond.


As for now 40 practice trials and 96 test trials are run. 

Each visual target is presented for 500 ms. (as far as I can see, there is no
information regarding target duration in the paper). After response there is 
a 500 ms. response-to-stimulus interval.

Tha task is to respond to targets (i.e., q for a circle, w for an X,
 a for a triangle, and s for a square). If the figure is blue
 participants are to respond to the global figure. In the example below press
 'a' (triangle)
                             
                                 O
                                O O
                               O   O
                              O     O
                             O O O O O
                             
If the target is black participants are to respond to the local fiugre. In
the example above press 'q' (circle) .

50 % of each trials are switch trials meaning that it requires a switch of 
mental set.  This quasi-randomization is done for each participant in
 contrast to prerandomized as in the paper.
"""

from psychopy import visual, event ,core,data,gui, sound
import os, glob, csv, re
from fileHandling import *
from random import randint
from collections import Counter

class Window():
    
    def __init__(self, name = "Local-Global Task"):
        self.name = name
        
    def expWin(self, color):
        '''For creating the experiment window
        in preferred color
        self.color = color
        '''
        self.color = color
        self.win = visual.Window(size=(840, 840), fullscr=False, screen=0, 
                                 allowGUI=False, allowStencil=False,
            monitor=u'testMonitor', color=self.color, colorSpace=u'rgb',
            blendMode=u'avg',winType=u'pyglet')     
        return self.win
        
    def expInfo(self, expName = "SET EXPERIMENT NAME"):
        self.expName = expName   
        self.expInfo = {'Subject Id':'', 'Age':'', 'Experiment Version': 0.1,
                        'Sex': ['Male', 'Female', 'Other']}
        self.expInfo[u'date'] = data.getDateStr(format="%Y-%m-%d_%H:%M")  
        self.infoDlg = gui.DlgFromDict(dictionary=self.expInfo, 
                                       title=self.expName,
                                       fixed=['Experiment Version'])
        self.expInfo[u'DataFile'] = u'Data' + os.path.sep + u'DATA_Local-Global_Task.csv'
        if self.infoDlg.OK:
            return self.expInfo
        else: 
            return 'Cancelled'
            
class Task():
    def __init__(self, nExpTrials, nPracTrials):
        self.xTrials = nExpTrials
        self.pTrials = nPracTrials

    def createTrialList(self,listostim, ntrials):
        '''
        Will randomize 50 % of shifting trials
        based on that each filename (of the images) starts with Black or Blue-.
        
        listostim is a list of trials
        ntrials is an integer indicating number of trials
        '''
        stimList = listostim
        nEachstim = ntrials/len(stimList)
        nEachtype = ntrials/2
        trialTypes = []
        stims = []
        countOfStim = dict((el,0) for el in stimList)
        count = {'ns':0,'s':0}
        for i in range(ntrials):
            shuffle(stimList)
            for idx in range(len(stimList)):
                if not stims:
                    countOfStim[stimList[idx]] +=1
                    stims.append(stimList[idx])
                    count['ns'] +=1
                    trialTypes.append("No-Shifting")
                elif stims:
                    if count['s'] <= nEachtype:
                        if countOfStim[stimList[idx]] <= nEachstim-1:
                            if stimList[idx][:5] != stims[i-1][:5]:
                                count['s'] +=1
                                countOfStim[stimList[idx]] +=1
                                stims.append(stimList[idx])
                                trialTypes.append("Shifting")
            
                            else:
                                count['ns'] +=1
                                countOfStim[stimList[idx]] +=1
                                stims.append(stimList[idx])
                                trialTypes.append("No-Shifting")
                    elif count['s'] > nEachtype:
                        if countOfStim[stimList[idx]] <= nEachstim-1: 
                            if stimList[idx][:5] == stims[i-1][:5]:
                                count['ns'] +=1
                                countOfStim[stimList[idx]] +=1
                                stims.append(stimList[idx])
                                trialTypes.append("No-Shifting")
        #Frequency of the trialtypes
        freq = Counter(trialTypes).values()
        if freq[0] == freq[1] and sum(freq) == ntrials:
            return stims
        elif freq[0] != nEachtype and freq[1] !=nEachtype or sum(freq) !=ntrials:
            return self.createTrialList(stimList, ntrials)

    
    def CreateExpTrials(self, trialList, expinfo, files, practice=False):
        '''
        Creates the experimental trials
        '''
        self.exp = expinfo
        trials = trialList
        trialList = []
        #1 = 
        listOfResps = ['q','w','a', 's']
        if practice:
                expTask = "Practice"
        else:
                expTask = "Experimental"
                
        for trial, target in enumerate(trials):#Here i could use enumerate(trial, trialSeq)
            parts = re.findall(r"[^\W_']+", target)
            if parts[0] == "Blue":
                TrialType = 'Global'
                if parts[1] == "Circle":
                    self.correctResp = listOfResps[0]
                elif parts[1] == "X":
                    self.correctResp = listOfResps[1]
                elif parts[1] == "Triangle":
                    self.correctResp = listOfResps[2]
                elif parts[1] == "Rect":
                    self.correctResp = listOfResps[3]

            elif parts[0] == "Black":
                TrialType = 'Local'
                if parts[2] == "Circle":
                    self.correctResp = listOfResps[0]
                elif parts[2] == "X":
                    self.correctResp = listOfResps[1]
                elif parts[2] == "Triangle":
                    self.correctResp = listOfResps[2]
                elif parts[2] == "Rect":
                    self.correctResp = listOfResps[3]

            trialList.append({'Cresp':self.correctResp, 
                                  u'File':files[target][1],
                                   u'Stimulus':files[target][0], 
                                   u'Trial':trial+1,
                                   u'Sub_id':self.exp['Subject Id'],
                                     u'Age':self.exp['Age'], 
                                     u'Sex':self.exp['Sex'], 
                                        u'TrialType':TrialType, 
                                        u'Task':expTask,
                                     u'Date':self.exp['date']})
        trialHandler = data.TrialHandler(trialList,1, method="sequential")  
        trialHandler.data.addDataType('Response')
        trialHandler.data.addDataType('Accuracy')
        trialHandler.data.addDataType('RT')  
        return trialHandler
    
    def runTrials(self, trialObj, frameR, win, datafile,load):
        frameR = frameR
        trialhandler = trialObj
        self.win = win
        self.timer = core.Clock()
        self.targetFrames = int(frameR * .5)
        self.itiFrames = int(frameR * .5)
        for trial in trialhandler:
            self.timer.reset()
            for frame in range(self.targetFrames):
                    visualTarget = trial['Stimulus']
                    self.presStim('image', visualTarget)

            self.presStim('text', '+')
            keys = event.waitKeys(keyList=['q','w','a', 's'])
            if keys:  
                trial['RT'] = self.timer.getTime()
                if keys[0] == trial['Cresp']: 
                    trial['Accuracy'] = 1
                else: 
                    trial['Accuracy'] = 0
                trial['Response'] = keys[0]
                trial['RT'] = self.timer.getTime()
                load.writeCsv(fileName=datafile, thisTrial=trial)
            for frame in range(self.itiFrames):
                self.presStim('text', '+')

    def txtStim(self, win, text, pos, name, height, color):
        '''Creates a text stimulus,
        self.text = text
        self.pos = pos
        self.name = name
        self.height = height
        self.color = color'''
        
        self.text = text
        self.pos = pos
        self.name = name
        self.height = height
        self.color = color
        textStim = visual.TextStim(win=self.win, ori=0, name=self.name,
            text=self.text,    font=u'Arial',
            pos=self.pos, height=self.height,
            color=self.color, colorSpace=u'rgb') 
        return textStim           
    
    def presStim(self, stim, target):
        self.stim = stim
        self.target = target
        self.win.flip()  
        textOnScreen = self.txtStim(self.win, text='',
                                     pos=[0.0,0.0], name='Visual Target',
                                     height=0.07, color='Black')
        if self.stim == "text":
            textOnScreen.setText(target)
            textOnScreen.draw()
        elif self.stim == "image":
            self.target.draw()
    def instructions(self, win):
        win.flip()
        event.waitKeys()
        event.clearEvents()
        core.wait(1)

def main():
    winz = Window()
    info = winz.expInfo(expName = "Local-Global Task")
    load = fileHandling()
    load.makeDir('Data')
    task = Task(96,40)
    win = winz.expWin(color="white")
    frameR = win.getActualFrameRate()
    files = load.loadFiles('stimuli', '.png', 'image', win)
    keyList = [key for key in files]
    txtfile = load.loadFiles("instructions", "txt", "text", win)
    txtfile['instruk'].draw()
    task.instructions(win)
    #Practice Trials
    pracList = task.createTrialList(keyList, 40)
    pracHand = task.CreateExpTrials(pracList, info, files,  practice=True)
    task.runTrials(pracHand, frameR, win, info['DataFile'], load)
    core.wait(.5)
    #Experimental Trials
    stimList = task.createTrialList(keyList, 96)
    trialhand =  task.CreateExpTrials(stimList, info, files)
    task.runTrials(trialhand, frameR, win, info['DataFile'], load)
    core.quit()
if __name__ == "__main__":
    main()        
