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
from psychopy import visual, event ,core,data,gui
import os, re
from fileHandling import *
from collections import Counter

class Window():
    
    def __init__(self, name = "Local-Global Task"):
        self.name = name
        
    def createWindow(self, color):
        '''For creating the experiment window
        in preferred color
        self.color = color
        '''
        self.color = color
        self.win = visual.Window(size=(1080, 1080), fullscr=False, screen=0, 
                                 allowGUI=False, allowStencil=False,
            monitor=u'testMonitor', color=self.color, colorSpace=u'rgb',
            blendMode=u'avg',winType=u'pyglet')     
        return self.win
        
    def experimentInfo(self, expName = "SET EXPERIMENT NAME"):
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

    def randomizeTargets(self,targets, ntrials):
        '''
        Will randomize 50 % of shifting trials
        based on that each filename (of the images) starts with Black or Blue-.
        
        listostim is a list of trials
        ntrials is an integer indicating number of trials
        '''
        nEachstim = ntrials/len(targets)
        wantedNeachType = ntrials/2
        trialTypes = []
        targetTrials = []
        countOfTargets = dict((el,0) for el in targets)
        countOfTrialTypes = {'ns':0,'s':0}
        targetsAndTrialTypes = []
        
        for i in range(ntrials):
            shuffle(targets)
            for idx in range(len(targets)):
                if not targetTrials:
                    countOfTargets[targets[idx]] +=1
                    targetTrials.append(targets[idx])
                    countOfTrialTypes['ns'] +=1
                    trialTypes.append("No-Shifting")
                elif targetTrials:
                    if countOfTrialTypes['s'] <= wantedNeachType:
                        if countOfTargets[targets[idx]] <= nEachstim-1:
                            if targets[idx][:5] != targetTrials[i-1][:5]:
                                countOfTrialTypes['s'] +=1
                                countOfTargets[targets[idx]] +=1
                                targetTrials.append(targets[idx])
                                trialTypes.append("Shifting")
            
                            else:
                                countOfTrialTypes['ns'] +=1
                                countOfTargets[targets[idx]] +=1
                                targetTrials.append(targets[idx])
                                trialTypes.append("No-Shifting")
                    elif countOfTrialTypes['s'] > wantedNeachType:
                        if countOfTargets[targets[idx]] <= nEachstim-1: 
                            if targets[idx][:5] == targetTrials[i-1][:5]:
                                countOfTrialTypes['ns'] +=1
                                countOfTargets[targets[idx]] +=1
                                targetTrials.append(targets[idx])
                                trialTypes.append("No-Shifting")
                                
        #Frequency of the trialtypes
        nEachTrialType = Counter(trialTypes).values()
        if nEachTrialType[0] == nEachTrialType[1] and sum(nEachTrialType) == ntrials:
            targetsAndTrialTypes.append(targetTrials)
            targetsAndTrialTypes.append(trialTypes)
            return targetsAndTrialTypes
        elif nEachTrialType[0] != wantedNeachType and nEachTrialType[1] !=wantedNeachType or sum(nEachTrialType) !=ntrials:
            return self.randomizeTargets(targets, ntrials)
    
    def createExperimentTrials(self, trialsAndTypes, expinfo, files, practice=False):
        '''
        Uses PsychoPy's trialhandler
        trialsAndTypes is a list containing 2 lists. First is a list of strings
        for the Targets. Second is a list of TrialTypes
        expinfo contains the info of the experiment to be saved,
        files is the object with the images
        '''
        trialTypes = trialsAndTypes[1]
        trialTargets = trialsAndTypes[0]
        experimentTrials = []
        responseKeys = ['q','w','e', 'r']
        if practice:
                expTask = "Practice"
        else:
                expTask = "Experimental"
                
        for trialNumber, target in enumerate(trialTargets):
            parts = re.findall(r"[^\W_']+", target)
            if parts[0] == "Blue":
                taskType = 'Global'
                if parts[1] == "Circle":
                    correctResponse = responseKeys[0]
                elif parts[1] == "X":
                    correctResponse = responseKeys[1]
                elif parts[1] == "Triangle":
                    correctResponse = responseKeys[2]
                elif parts[1] == "Rect":
                    correctResponse = responseKeys[3]
            elif parts[0] == "Black":
                taskType = 'Local'
                if parts[2] == "Circle":
                    correctResponse = responseKeys[0]
                elif parts[2] == "X":
                    correctResponse = responseKeys[1]
                elif parts[2] == "Triangle":
                    correctResponse = responseKeys[2]
                elif parts[2] == "Rect":
                    correctResponse = responseKeys[3]

            experimentTrials.append({'Cresp':correctResponse, 
                                  u'File':files[target][1],
                                   u'Stimulus':files[target][0], 
                                   u'Trial':trialNumber+1,
                                   u'Sub_id':expinfo['Subject Id'],
                                     u'Age':expinfo['Age'], 
                                     u'Sex':expinfo['Sex'], 
                                        u'TaskType':taskType, 
                                        u'Task':expTask,
                                        u'TrialType':trialTypes[trialNumber],
                                     u'Date':expinfo['date']})
        trialHandler = data.TrialHandler(experimentTrials,1, method="sequential")  
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
                    self.presentStimulus('image', visualTarget)

            self.presentStimulus('text', '+')
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
                self.presentStimulus('text', '+')

    def createTextStimulus(self, win, text, pos, name, height, color):
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
    
    def presentStimulus(self, stim, target):
        self.stim = stim
        self.target = target
        self.win.flip()  
        textOnScreen = self.createTextStimulus(self.win, text='',
                                     pos=[0.0,0.0], name='Visual Target',
                                     height=0.07, color='Black')
        if self.stim == "text":
            textOnScreen.setText(target)
            textOnScreen.draw()
        elif self.stim == "image":
            self.target.draw()
    def waitForKyes(self, win):
        win.flip()
        event.waitKeys()
        event.clearEvents()
        core.wait(.2)

def main():
    experimentWindow = Window()
    info = experimentWindow.experimentInfo(expName = "Local-Global Task")
    load = fileHandling()
    load.makeDir('Data')
    task = Task(96,40)
    win = experimentWindow.createWindow(color="white")
    frameRate = win.getActualFrameRate()
    files = load.loadFiles('stimuli', '.png', 'image', win)
    visualTargets = [key for key in files]
    txtfile = load.loadFiles("instructions", "txt", "text", win)
    txtfile['instruk'].draw()
    task.waitForKyes(win)
    #Practice Trials
    practiceTargets = task.randomizeTargets(visualTargets, 40)
    pracHand = task.createExperimentTrials(practiceTargets, info, 
                                           files,  practice=True)
    task.runTrials(pracHand, frameR, win, info['DataFile'], load)
    core.wait(.5)
    txtfile['exptask'].draw()
    task.waitForKyes(win)
    #Experimental (test) Trials
    testTargets = task.randomizeTargets(visualTargets, 96)
    trialhand =  task.createExperimentTrials(testTargets, info, files)
    task.runTrials(trialhand, frameRate, win, info['DataFile'], load)
    core.wait(.5)
    txtfile['thanks'].draw()
    task.waitForKyes(win)
    core.quit()
    
if __name__ == "__main__":
    main()        
