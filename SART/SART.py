# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 22:05:30 2015
Sustained Attention to Response Task & Vigalance Task

@author: erik @ marsja dot se
"""

from psychopy import visual, core, data, sound, gui, event
import glob, os

from random import shuffle

class Experiment():
    '''
    Two tasks;

    1)Sustained Attention To Response task
    Robertson et al., (1997)
    x digits (x pairs of x digits)
    Each digit is presented for 250 Msec followed by a 900 Msec mask
    (Mask= ring with diaognoal cross in the middle, diameter=29mm).

    Digit 3 is no response digit, prefixed quasi-randomly distributed among x trials

    Digit onset-to-onset 1150 ms

    2)Vigilance task (modified SART)
    Same as above but responses on digit 3 only (withold on all other digits)
    '''

    def __init__(self, digits, nTrials, name):
        #Should look this over and probably change it
        self.name = name
        self.nDigits = digits
        self.digits = range(1,digits+1)
        self.trials = nTrials

    def createTrials(self):
        '''Creates a list of trials.
        '''
        trials = []
        for trialSequence in range(self.trials/self.nDigits):
            shuffled = self.digits[:]
            shuffle(shuffled)
            trials.append(shuffled)
        return trials

    def experimentWindow(self, color):
        '''For creating the experiment window
        in preferred color
        self.color = color
        '''
        self.win = visual.Window(size=(1920, 1200), fullscr=True, screen=0,
                                 allowGUI=False, allowStencil=False,
            monitor=u'testMonitor', color=color, colorSpace=u'rgb',
            blendMode=u'avg',winType=u'pyglet')
        return self.win

    def createTextStimulus(self, win, text, pos, name, height, color):
        '''Creates  text stimulu1,
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
        textStimulus = visual.TextStim(win=self.win, ori=0, name=self.name,
            text=self.text,    font=u'Arial',
            pos=self.pos, height=self.height,
            color=self.color, colorSpace=u'rgb')
        return textStimulus

    def presentStimulus(self, stim, target):
        self.stimulus = stim
        self.target = target
        self.win.flip()
        if self.stimulus == "text":
            self.textOnScreen.setText(target)
            self.textOnScreen.draw()
        elif self.stimulus == "image":
            self.target.draw()
        elif self.stimulus == "sound":
            '''here we will we play the sound
            NOT IMPLEMENTED YET
            '''
            self.target.play()

    def experimentTrials(self, trials, expinfo):
        self.exp = expinfo
        self.trialList = []
        self.correctresp = 'space'

        for trialSequence in trials:
            for trial, digit in enumerate(trialSequence):
                trial +=1
                if digit == 3:
                    if self.expinfo['Task'] == 'SART':
                        self.correctresp = u'Noresponse'
                    elif self.expinfo['Task'] == 'Vigilance':
                        self.correctresp = u'space'

                else:
                    if self.expinfo['Task'] == 'SART':
                        self.correctresp = u'space'
                    elif self.expinfo['Task'] == 'Vigilance':
                        self.correctresp = u'Noresponse'

                self.trialList.append({'Cresp':self.correctresp,
                                       u'Stimulus':digit, u'Trial':trial,
                                       u'Sub_id':self.exp['Subject Id'],
                                         u'Age':self.exp['Age'],
                                         u'Sex':self.exp['Sex'],
                                         u'Date':self.exp['date'],
                                         u'Task':self.expinfo['Task']})
        self.trialHandler = data.TrialHandler(self.trialList,1, method="sequential")
        self.trialHandler.data.addDataType('Response')
        self.trialHandler.data.addDataType('Accuracy')
        self.trialHandler.data.addDataType('RT')
        return self.trialHandler

    def experimentInfo(self):
        self.expName = u'Sustained attention'
        self.expInfo = {'Subject Id':'', 'Age':'', 'ExpVersion': 0.2,
                        'Sex': ['Male', 'Female'], 'Task':['SART', 'Vigilance']}
        self.expInfo[u'date'] = data.getDateStr(format="%Y-%m-%d_%H:%M")
        self.infoDlg = gui.DlgFromDict(dictionary=self.expInfo,
                                       title=self.expName, fixed=['ExpVersion'])
        self.datafile = u'Data' + os.path.sep + u'DATA_SART.csv'
        if self.infoDlg.OK:
            return self.expInfo
        else:
            return 'Cancelled'

    def runTrials(self, trialObj):
        self.trialhandler = trialObj
        self.timer = core.Clock()
        self.targetFrames = int(self.frameR * .25)
        self.itiFrames = int(self.frameR * .9)
        for trial in self.trialhandler:
            self.timer.reset()
            for frame in range(self.targetFrames):
                    visualTarget = trial['Stimulus']
                    self.presentStimulus('text', visualTarget)
            for frame in range(self.itiFrames):
                    self.presentStimulus('image', self.mask)
                    keys = event.getKeys(keyList=['space'])
                    if keys:
                        trial['RT'] = self.timer.getTime()
                        if keys[0] == trial['Cresp']:
                            trial['Accuracy'] = 1
                        else:
                            trial['Accuracy'] = 0

            trial['RT'] = self.timer.getTime()
            trial['Accuracy'] = 0
            self.writeCsv(self.datafile, trial)

    def writeCsv(self,fileName, thisTrial):
        import codecs, csv, os
        fullPath = os.path.abspath(fileName)
        if not os.path.isfile(fullPath):
            with codecs.open(fullPath, 'ab+', encoding='utf8') as f:
                csv.writer(f, delimiter=';').writerow(thisTrial.keys())
                csv.writer(f, delimiter=';').writerow(thisTrial.values())
        else:
            with codecs.open(fullPath, 'ab+', encoding='utf8') as f:
                csv.writer(f, delimiter=';').writerow(thisTrial.values())
    def makeDir(self, dirname):
        import os
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

    def runExperiment(self):
        self.makeDir('Data')
        self.expinfo = self.experimentInfo()
        if self.expinfo == 'Cancelled':
            print 'User cancelled'
            core.quit()

        self.win = self.experimentWindow(color = 'black')
        self.frameR = self.win.getActualFrameRate()

        if not self.frameR:
            self.frameR = 60.0
            
        self.load = preLoading()
        self.files = self.load.loadFiles("Stimuli", "png", "image", self.win)
        self.txtfiles = self.load.loadFiles("Stimuli", "txt", "text", self.win)
        self.mask = self.files['circleMask'][0]
        self.textOnScreen = self.createTextStimulus(self.win, text='',
                                         pos=[0.0,0.0], name='Visual Target',
                                         height=0.07, color='White')
        self.txtfiles[self.expinfo['Task']].draw()
        self.win.flip()
        event.waitKeys()
        event.clearEvents()
        self.trials = self.createTrials()
        trialsToRun = self.experimentTrials(self.trials, self.expinfo)
        self.runTrials(trialsToRun)
        core.quit()

class preLoading():

    def __init__(self):
        self.path = os.getcwd()

    def loadFiles(self, directory,extension,fileType,win='',whichFiles='*',stimList=[]):
        """ Load all the pics and sounds"""
        self.dir = directory
        self.extension = extension
        self.fileType = fileType
        self.wi = win
        self.whichFiles = whichFiles
        self.stimList=stimList

        if isinstance(self.extension,list):
            fileList = []
            for curExtension in self.ext:
                print self.whichFiles
                fileList.extend(glob.glob(
                                        os.path.join(self.path,
                                                       self.directory,
                                                       self.whichFiles+curExtension)))
        else:
            fileList = glob.glob(os.path.join(self.path,directory,self.whichFiles+self.extension))
            fileMatrix = {} #initialize fileMatrix  as a dict because it'll be accessed by picture names, cound names, whatver
        for num,curFile in enumerate(fileList):
            fullPath = curFile
            fullFileName = os.path.basename(fullPath)
            stimFile = os.path.splitext(fullFileName)[0]
            if fileType=="image":
                from psychopy import visual
                try:
                    surface = pygame.image.load(fullPath) #gets height/width of the image
                    stim = visual.SimpleImageStim(win, image=fullPath)
                    fileMatrix[stimFile] = ((stim,fullFileName,num,surface.get_width(),surface.get_height(),stimFile))
                except: #no pygame, so don't store the image dims
                    stim = visual.SimpleImageStim(win, image=fullPath)
                    fileMatrix[stimFile] = ((stim,fullFileName,num,'','',stimFile))
            elif fileType=="sound":
                soundRef = sound.Sound(fullPath)
                fileMatrix[stimFile] = ((soundRef))
            elif fileType=='text':
                from psychopy import visual
                import codecs
                with codecs.open(fullPath, 'r', encoding='utf8') as f:
                    textRef = visual.TextStim(win, text=f.read(), wrapWidth=1.2, alignHoriz='center', alignVert='center', height=0.06)

                fileMatrix[stimFile] = ((textRef))

        #check
        if stimList and set(fileMatrix.keys()).intersection(stimList) != set(stimList):
            popupError(str(set(self.stimList).difference(fileMatrix.keys())) + " does not exist in " + self.path+'\\'+directory)

        return fileMatrix
def main():
    test = Experiment(digits=9, nTrials=225, name="Sustained Attention")
    test.runExperiment()

if __name__ == "__main__":
    main()
