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
import os, re
from collections import Counter
from random import shuffle

from psychopy import visual, event ,core,data,gui
from fileHandling import *

class Window():
    
    def __init__(self, name = "Local-Global Task"):
        self.name = name
        
    def create_window(self, color):
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
        
    def get_subj_information(self, expName = "SET EXPERIMENT NAME"):
        self.expName = expName   
        self.subj_information = {'Subject Id':'', 'Age':'', 
                'Experiment Version': 0.1, 'Sex': ['Male', 'Female', 'Other']}
        self.subj_information[u'date'] = data.getDateStr(format="%Y-%m-%d_%H:%M")  
        self.infoDlg = gui.DlgFromDict(dictionary=self.subj_information, 
                                       title=self.expName,
                                       fixed=['Experiment Version'])
        self.subj_information[u'DataFile'] = u'Data' + os.path.sep + u'DATA_Local-Global_Task.csv'
        if self.infoDlg.OK:
            return self.subj_information
        else: 
            return 'Cancelled'
            
class Task():
    def __init__(self, nExpTrials, nPracTrials):
        self.xTrials = nExpTrials
        self.pTrials = nPracTrials

    def randomize_targets(self,listostim, ntrials):
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
        returnList = []
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
            returnList.append(stims)
            returnList.append(trialTypes)
            return returnList
        elif freq[0] != nEachtype and freq[1] !=nEachtype or sum(freq) !=ntrials:
            return self.randomize_targets(stimList, ntrials)
    
    def create_trials(self, trialsAndTypes, expinfo, files, practice=False):
        '''
        Creates the experimental trials
        uses PsychoPy's trialhandler
        trialsAndTypes is a list containing 2 lists. First is a list of strings
        for the Targets. Second is a list of TrialTypes
        expinfo contains the info of the experiment to be saved,
        files is the object with the images
        '''
        trialTypes = trialsAndTypes[1]
        self.exp = expinfo
        trials = trialsAndTypes[0]
        trialList = []
        listOfResps = ['q','w','e', 'r']
        if practice:
                expTask = "Practice"
        else:
                expTask = "Experimental"
                
        for trial, target in enumerate(trials):#Here i could use enumerate(trial, trialSeq)
            parts = re.findall(r"[^\W_']+", target)
            if parts[0] == "Blue":
                taskType = 'Global'
                if parts[1] == "Circle":
                    self.correctResp = listOfResps[0]
                elif parts[1] == "X":
                    self.correctResp = listOfResps[1]
                elif parts[1] == "Triangle":
                    self.correctResp = listOfResps[2]
                elif parts[1] == "Rect":
                    self.correctResp = listOfResps[3]
            elif parts[0] == "Black":
                taskType = 'Local'
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
                                        u'TaskType':taskType, 
                                        u'Task':expTask,
                                        u'TrialType':trialTypes[trial],
                                     u'Date':self.exp['date']})
        trialHandler = data.TrialHandler(trialList,1, method="sequential")  
        trialHandler.data.addDataType('Response')
        trialHandler.data.addDataType('Accuracy')
        trialHandler.data.addDataType('RT')  
        return trialHandler
    
    def run_trials(self, trialObj, frameR, win, datafile,load):
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
                    self.present_stimulus('image', visualTarget)

            self.present_stimulus('text', '+')
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
                self.present_stimulus('text', '+')

    def create_text_stimuli(self, win, text, pos, name, height, color):
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
    
    def present_stimulus(self, stim, target):
        self.stim = stim
        self.target = target
        self.win.flip()  
        textOnScreen = self.create_text_stimuli(self.win, text='',
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
        core.wait(.2)

def main():
    winz = Window()
    info = winz.get_subj_information(expName = "Local-Global Task")
    load = fileHandling()
    load.makeDir('Data')
    task = Task(96,40)
    win = winz.create_window(color="white")
    frameR = win.getActualFrameRate()
    files = load.loadFiles('stimuli', '.png', 'image', win)
    keyList = [key for key in files]
    txtfile = load.loadFiles("instructions", "txt", "text", win)
    txtfile['instruk'].draw()
    task.instructions(win)
    #Practice Trials
    pracList = task.randomize_targets(keyList, 40)
    pracHand = task.create_trials(pracList, info, files,  practice=True)
    task.run_trials(pracHand, frameR, win, info['DataFile'], load)
    core.wait(.5)
    txtfile['exptask'].draw()
    task.instructions(win)
    #Experimental Trials
    stimList = task.randomize_targets(keyList, 96)
    trialhand =  task.create_trials(stimList, info, files)
    task.run_trials(trialhand, frameR, win, info['DataFile'], load)
    core.wait(.5)
    txtfile['thanks'].draw()
    task.instructions(win)
    core.quit()
if __name__ == "__main__":
    main()        
