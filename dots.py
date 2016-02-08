import numpy as np
from psychopy import visual, core, event, monitors


class spatialWM():
    def createWin(self):
        from psychopy import visual, monitors
        self.mon = monitors.Monitor('My screen', width=37.5, distance=57)
        self.mon.setSizePix((1280,1024))
        self.win = visual.Window(color='lightgray', units='deg', monitor=self.mon)
        return self.win
        
    def expInfo(self):
        import os
        from psychopy import data, gui
        self.expName = u'Spatial WM task'   
        self.expInfo = {'Subject Id':'', 'Age':'', 'ExpVersion': 0.1,
                        'Sex': ['Male', 'Female']}
        

        self.expInfo[u'date'] = data.getDateStr(format="%Y-%m-%d_%H:%M")  
        self.infoDlg = gui.DlgFromDict(dictionary=self.expInfo, 
                                       title=self.expName, fixed=['ExpVersion'])
        self.datafile = u'Data' + os.path.sep + u'_SART.csv'
        if self.infoDlg.OK:
            return self.expInfo
        else: 
            return 'Cancelled'
    def dotPos(self, radius, ncircles):
        self.r = radius  # radius of the larger circle
        self.ncircles = ncircles
        angle = 2 * np.pi / ncircles
        self.positions = []
        for i in range(ncircles):
            pos = (self.r*np.cos(angle*i), self.r*np.sin(angle*i))
            self.positions.append(pos)
        print self.positions
        return self.positions
        
    def genProbes(self, nTrials, nProbes):
        '''Each position need to be equally probed
        returns position for trial in each condition        
        '''
        from random import randint as rand
        numberOfprobes = len(nTrials)/nProbes #To get how many probes/serial position
        
        #create a dict with the probes to keep count
        probes = {}
        probeList = [] #to store each trials probe...
        for i in range(nProbes):
            probes[i]=0

        for i in range(len(nTrials)):
     
            serialposition = rand(0,nProbes-1)#getting an index to randomly 
            while probes[serialposition] == numberOfprobes:
                serialposition = rand(0,nProbes-1)
              
            probeList.append(serialposition)
            probes[serialposition] += 1
      
        return probeList
        
    def trialList(self, nTrials, positions):
        from random import randint
        self.nTrials = nTrials
        self.pos = positions
        self.trialList = []
        #One position will not be used in each trial = 9 positions in each trial
        for trial in range(self.nTrials):
            targetlist = []
            for i in range(len(self.pos)-1):
                idx = randint(0,len(self.pos)-1)
                targetlist.append(self.pos[idx])
            self.trialList.append(targetlist)
        return self.trialList
        
    def expTrials(self, trialList, expinfo):
        from psychopy import data
        self.exp = expinfo
        self.probes = self.genProbes(self.trialList, 8)
        
        self.trialList = []
        trial = 0
        stimList=[]
        block = 01
        for line in trialList:
            targetList=[]
            for i in range(len(line)):
                targetList.append(line[i])
            #Which serial position is the correct target on?
            probeIdx =self.probes[trial]
            stimList.append(
            {'Sub_id': self.exp['Subject Id'], 'Age':self.exp['Age'], 'Sex':self.exp['Sex'],'TargetsTrial':line, 'Trial':str(trial+1), 'Block': block+1, 'Target':targetList, 'Probe':targetList[probeIdx], 
            'Probe-SerialPosition':self.probes[trial]})
            trial+=1
            
        self.trialHandler = data.TrialHandler(stimList,1, method="sequential")  
        self.trialHandler.data.addDataType('Response')
        self.trialHandler.data.addDataType('Accuracy')
        self.trialHandler.data.addDataType('RT')  
        return self.trialHandler
        
    def runTrials(self, trials):
        self.runTrials=trials
        frameRate =self.expInfo['frameRate']  # Set your screens framerate in Hz
        targetDuration = 1.0  # ms
        xDuration = .4 # ms ISI (digits)
        wDuration =.5 #ms
        fDuration = 1.5  # ms
        targetFrames = int(frameRate * targetDuration) #For digits
        isiFrames = int(frameRate * xDuration)
        wFrames = int(frameRate * wDuration)
        fixationFrames = int(frameRate * fDuration)
        gapFrames = int(frameRate * 0.1)
        vibFrames = int(frameRate * 0.3)#I set this for now to .03 to include the gap...
        frameN = -1
        for thisTrial in self.runTrials:
            frameN = frameN + 1
            #Warning for begin trial...
#            warned = True
#
#            while warned:
#                warnRect.draw()
#                warning1.draw()
#                self.win.flip()
#                if myMouse.isPressedIn(warnRect):
#                    warned = False
#            for frameN in range(wFrames):
#                warnRect.draw()
#                warning1.draw()
#                win.flip()
            #Fixation cross
            for frameN in range(fixationFrames):
        
                self.textOnScreen.setText('+')
                self.textOnScreen.draw()
                self.win.flip()
            #Trial starts 
            for i in range(len(thisTrial['TargetsTrial'])):
                
                #Vibration based on which condition 
#                try:
#                    len(thisTrial['Vibration'])>1
#                    if i%2==0:
#                        vib = thisTrial['Vibration'][0]
#                    else: vib = thisTrial['Vibration'][1]
#                except: vib = thisTrial['Vibration']
                #Drawing target on screen
                for frameN in range(targetFrames):
                    self.circle.pos = thisTrial['Target'][i]
                    self.circle.draw()
                    self.win.flip()
                    
                for frameN in range (isiFrames):
                    self.textOnScreen.setText('')
                    self.textOnScreen.draw()
                    self.win.flip()
        
#                    if frameN == gapFrames:
#                        #Starting vibration after the gap...
#                        port.setData(vib)
#                        
#                    if frameN == vibFrames:
#                        #Stopping the vibration after 300 (but the duration is only 200 ms!)
#                        port.setData(0)
                    thisTrial['SerialPosition' + str(i+1)] = thisTrial['TargetsTrial']

            #Retention(?)
            for frameN in range(targetFrames):
                    self.win.flip()
            #RTclock.reset()
            #thisTrial['Response'] = dispResp()
            #thisTrial['RT'] = RTclock.getTime()
            #Check if correct response was made
            #if thisTrial['Probe'] == Target To the right of probe
              #  thisTrial['Accuracy'] = 1
            #else:
               # thisTrial['Accuracy'] = 0
            #save data for each subject in same file?    
           # writeCsv(datafile, thisTrial)
            #Handling blocks
            if trials.getFutureTrial():
                nextTrial = trials.getFutureTrial(n=1) 
            if nextTrial['Block'] != thisTrial['Block']:
        
                self.textOnScreen.setText('Take a short break. Press any key on the keyboard to continue')
                textOnScreen.draw()
                win.flip()
                event.clearEvents()
                event.waitKeys()
            if  not trials.getFutureTrial():
               win.flip()
               event.clearEvents()

    def runExp(self):
        from psychopy import event
        self.expInfo = self.expInfo()
        self.win = self.createWin()
        self.expInfo[u'frameRate']=self.win.getActualFrameRate()

        self.targetPos = self.dotPos(8, 10)
        self.probePos = self.dotPos(8, 10)
        self.circle = visual.Circle(self.win, radius=.25, fillColor='black', lineColor='black', pos=(0.0,0.0))
        self.probe = visual.Circle(self.win, radius=1, fillColor='lightgrey', lineColor='black', pos=(0.0,0.0))
        self.textOnScreen = visual.TextStim(self.win, text=None,
                                         pos=[0.0,0.0], name='Text On Screen',
                                         height=0.06, color='White')
        self.trialPos = self.trialList(24, self.targetPos)
        self.t = self.expTrials(self.trialPos, self.expInfo)
        self.runTrials(self.t)
        self.win.flip()
        event.waitKeys()
        self.win.close()
        
exp = spatialWM()
exp.runExp()