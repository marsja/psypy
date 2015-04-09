#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Serial Recall Probe Task
#Erik Marsja, erik at marsja.se (http://www.marsja.se)
#Import psychopy stuff
from psychopy import visual, event, core, logging, sound, gui, data
from psychopy.constants import * 
from psychopy import parallel as pp

#Python imports...
import time, os, re, random, glob
from datetime import datetime 
import numpy as np
from ast import literal_eval
#Import two of my custom made functions
from trialhandling import lsquare,blockOrder, genTrials, genProbes, writeCsv

def loadFiles(directory,extension,fileType,win='',whichFiles='*',stimList=[]):
    """ Load images"""
    path = os.getcwd() #set path to current directory
    if isinstance(extension,list):
        fileList = []
        for curExtension in extension:
            fileList.extend(glob.glob(os.path.join(path,directory,whichFiles+curExtension)))
    else:
        fileList = glob.glob(os.path.join(path,directory,whichFiles+extension))
        fileMatrix = {} #initialize fileMatrix  as a dict because it'll be accessed by picture names, cound names, whatver
    for num,curFile in enumerate(fileList):
        fullPath = curFile
        fullFileName = os.path.basename(fullPath)
        stimFile = os.path.splitext(fullFileName)[0]
        try:
            surface = pygame.image.load(fullPath) #gets height/width of the image
            stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
            fileMatrix[stimFile] = ((stim,fullFileName,num,surface.get_width(),surface.get_height(),stimFile))
        except: #no pygame, so don't store the image dims
            stim = visual.ImageStim(win, image=fullPath,mask=None,interpolate=True)
            fileMatrix[stimFile] = ((stim,fullFileName,num,'','',stimFile))

    if stimList and set(fileMatrix.keys()).intersection(stimList) != set(stimList):
        popupError(str(set(stimList).difference(fileMatrix.keys())) + " does not exist in " + path+'\\'+directory) 
    return fileMatrix

    if stimList and set(fileMatrix.keys()).intersection(stimList) != set(stimList):
        popupError(str(set(stimList).difference(fileMatrix.keys())) + u" does not exist in " + path+u'\\'+directory) 
    return fileMatrix
def dispResp():
    """Display probe """
    #Variables for handling "press the digit twice"...
    answered = True
    mousePressed = 0
    resp = ''
    #Response window drawn
    while answered:
        #The mouse cursor need to be visible..
        myMouse.setVisible(1)
        txt.draw()
        txt2.draw()
        answrect.draw()
        im, rect = {}, {}
        #Printing images in a row on the screen,
        #Also have some rectangles surrounding them (invisible)
        for i in range(len(vtargets)):
            im[str(i)] =  imStim(win=win, image=stimpath + vtargets[str(i)][1], pos=[xcords[i],0.0], name='Image' + str(i))
            rect[str(i)] = rectDraw(win=win, size=(.25,.35), pos=[xcords[i], 0.0],  lineCol='black', name='Rectangle' + str(i))
            im[str(i)].draw()
            rect[str(i)].draw()
        
        Probe.draw()
        #Checking which digit is pressed...
        for i in range(len(rect)):
            if myMouse.isPressedIn(rect[str(i)]):
                mousePressed += 1
                answrimg.setImage(stimpath + vtargets[str(i)][1])
                answrimg.name = str(i)
                answrimg.setAutoDraw(True)
        #If pressted twice record the response...  
        if mousePressed == 2:
            answrimg.setAutoDraw(False)
            resp = answrimg.name
            answered=False
            event.clearEvents()#DO I NEED THESE TWO LINES
            win.flip()                #SEE ABOVE
        win.flip()
    return resp

def imStim(win, image, pos, name):
    return visual.ImageStim(win=win, name=name,
        image=image, mask=None,
        ori=0, pos=pos,
        colorSpace=u'rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-5.0)

def txtStim(win, text, pos, name):
    return visual.TextStim(win=win, ori=0, name=name,
    text=text,    font=u'Arial',
    pos=pos, height=0.1, wrapWidth=None,
    color=u'black', colorSpace=u'rgb') 
def rectDraw(win, pos,size, lineCol, name):
    return visual.Rect(win= win, size=size, fillColor=None, lineColor=lineCol, pos=pos, name=name)

def makeDir(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)  # if this fails (e.g. permissions) we will get error

#Parallell output port (we will not have any input in this experiment)
port = pp.ParallelPort(address=0x1120) 

# Store info about the experiment session
expName = u'Serial Recall - Probe Task'  #
expInfo = {'Participant':'', 'Age':'', 'ExpVersion': 1.0, 'Block':1,'Sex': ['Male', 'Female']}
expInfo[u'date'] = data.getDateStr(format="%Y-%m-%d")  # add a simple timestamp
infoDlg = gui.DlgFromDict(dictionary=expInfo, title=expName, fixed=['ExpVersion'])

nTrials = 24 #Change this to set the amount of trials/condition. This number need to be dividable by 8

if infoDlg.OK:
    print expInfo
else: print 'User Cancelled'

#Data file handling
makeDir('Data')
makeDir('Data\\Subject_files')
filename = u'Data\\Subject_files' + os.path.sep + u'Data_%s_%s' %(expInfo[u'Participant'], expInfo[u'date'])
datafile = u'Data' + os.path.sep + u'Data_Serial_Recall_PT_exp1.csv'
logFile = logging.LogFile(filename+u'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

#Creating the experiment window
win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor=u'testMonitor', color=[255,255,255], colorSpace=u'rgb',
    blendMode=u'avg',useFBO=True,)

#Not using this right now...
expInfo[u'frameRate']=win.getActualFrameRate()
if expInfo[u'frameRate']!=None:
    frameDur = 1.0/round(expInfo[u'frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess
#Current path
curpath = os.getcwd()
stimpath = curpath + u'\\Stimuli\\'
#Clock for timing experiment
expClock = core.Clock()
#Clock for reaction time...
RTclock = core.Clock()

xcords = np.linspace(-0.6, 0.6, num =10)#Need to import numpy as np for doing this...
myMouse = event.Mouse() 
txt = u'Practice trials are over. Press any key to continue to test'
#To be put on the screen... fixation cross, warnings, etc...
warning1 =  txtStim(win, text=u'Begin', pos=[0.0,0.0], name=u'Warning')
endPractice = txtStim(win, text=txt, pos=[0.0,0.0], name=u'EndPractice')
fixation =  txtStim(win, text='+', pos=[0.0,0.0], name=u'Fixation')
txt = txtStim(win, text='What number came AFTER: ', pos=[-0.1,0.4], name='Question')
txt2 = txtStim(win, text='Press the digit two times. ', pos=[-0.1,0.3], name='Question')
#Shapes (i.e., rectangles)
answrect = rectDraw(win=win, size=(.3,.4), pos=[0.0, -0.3], lineCol='black', name='AnswerRectangle')
warnRect = rectDraw(win, pos=[0.0, 0.0],size=[.4,.25], lineCol='black', name='WarningRectangle')
#Target
Target =  imStim(win=win, image=None, pos=[0.0,0.0], name="Target")
#Probe
Probe =  imStim(win=win, image=None, pos=[0.32,0.40], name='Probe') 
#Answerimage
answrimg = imStim(win=win, image=None, pos=[0.0, -0.3], name=None)

vtargets = loadFiles('Stimuli','bmp','image',win)



#What blockorder? Using latin square design
#First a square design is done with the function. We have 3 conditions (cCount = 3!)
squares= lsquare(cCount=3) 

#Determining the order. Need to pass the square design, num of Partcipants and the current participant number
#Returns a list with 0,1,2 (0=baseline, 1=steady state, 2=changing state)
order = blockOrder(skv=squares, nParticipants=42, participant=int(expInfo['Participant']))

stimList = []

for block in range(3):
    count = 0
    trialList=genTrials(nTrials)
    probes = genProbes(trialList)
    if order[block] == 0:
        vib = 0
        condition = 'Quiet'
    elif order[block] == 1:
        vib = 5
        condition = 'Steady-state'
    elif order[block] == 2:
        #Balancing the order of vibrations... the first 14 participant will start with vibrations through the black handle 
        if int(expInfo['Participant']) in range(1,15) or int(expInfo['Participant']) in range(29,36): 
            vib = [1,4]#1 equals speed 1 to the "black" handle and 4 speed 1 to the "yellow" handle
        #The participants 14 through 28 eight (next 14) will start with yellow handle... and the last 7 as well...
        elif int(expInfo['Participant']) in range(15,29) or int(expInfo['Participant']) in range(36,43):
            vib = [4,1]
        condition = 'Changing-state'
    for line in trialList:
        targetList=[]
        for i in range(len(line)):
            index = line[i]
            sr = vtargets[str(index)]
            targetList.append(sr[1])
        #Which serial position is the correct target on?
        probeIdx =probes[count]
        stimList.append(
        {'Sub_id': expInfo['Participant'], 'Age':expInfo['Age'], 'Sex':expInfo['Sex'],'TargetsTrial':line, 'Trial':str(count+1), 'Block': block+1, 'VisualTarget':targetList, 'Probe':targetList[probeIdx][0], 
        'Probe-SerialPosition':probeIdx,'CorrectResponse':targetList[probeIdx+1][0],  'Vibration':vib, 'Condition':condition })
        count+=1

#Some durations. The duration of a frame (in seconds) is simply 1/refresh rate in Hz.
frameRate =expInfo['frameRate']  # Set your screens framerate in Hz
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

#Practice trials
#take two random trials from the stimList...
pracList = []
pracIdx = ''
for i in range(2):
    pracIdx = random.randint(0, len(stimList))
    pracList.append(stimList[pracIdx])
practice = data.TrialHandler(pracList,1, method="sequential")


#Trialhandler
trials = data.TrialHandler(stimList,1, method="sequential")#Trials are already randomized in the 
trials.data.addDataType('Response')
trials.data.addDataType('Accuracy')
trials.data.addDataType('RT')
#Timing the experiment...
expClock.reset()

for pos in range(1,10):
    trials.data.addDataType('SerialPosition' + str(pos))


#Show instructions;
Target.setImage(stimpath + 'taskinstructions.jpg')
Target.draw()
win.flip()
event.waitKeys()
event.clearEvents()

#PRACTICE: Right now it is running the 2 first testtrials...
frameN = -1

for thisTrial in practice:
    answrimg.setAutoDraw(False)
    frameN = frameN + 1
    #Warning for begin trial...
    warned = True
    while warned:
        warnRect.draw()
        warning1.draw()
        win.flip()
        if myMouse.isPressedIn(warnRect):
            warned = False
    for frameN in range(wFrames):
        warnRect.draw()
        warning1.draw()
        win.flip()
    #Fixation cross
    for frameN in range(fixationFrames):
        myMouse.setVisible(0)#Hide the mouse during presentation of target digits
        fixation.setText('+')
        fixation.draw()
        win.flip()
    #Trial starts 
    for i in range(len(thisTrial['TargetsTrial'])):
                 #Target
        Target.setImage(stimpath + thisTrial['VisualTarget'][i])

        for frameN in range(targetFrames):
            Target.setAutoDraw(True)
            
            win.flip()
        for frameN in range (isiFrames):  
            Target.setAutoDraw(False)
            fixation.setText('')
            fixation.draw()
            win.flip()
    #Setting the probe
    Probe.setImage(stimpath + thisTrial['Probe'] + '.bmp') 
    #Retention(?)
    for frameN in range(targetFrames):
            win.flip()

    thisTrial['Response'] = dispResp()
#END PRACTICE 
myMouse.setVisible(0)
endPractice.draw()
win.flip()
event.waitKeys()
event.clearEvents()

#Test starts...

frameN = -1
for thisTrial in trials:
    answrimg.setAutoDraw(False)
    frameN = frameN + 1
    #Warning for begin trial...
    warned = True
    myMouse.setVisible(1)
    while warned:
        warnRect.draw()
        warning1.draw()
        win.flip()
        if myMouse.isPressedIn(warnRect):
            warned = False
    for frameN in range(wFrames):
        warnRect.draw()
        warning1.draw()
        win.flip()
    #Fixation cross
    for frameN in range(fixationFrames):
        myMouse.setVisible(0)#Hide the mouse during presentation of target digits
        fixation.setText('+')
        fixation.draw()
        win.flip()
    #Trial starts 
    for i in range(len(thisTrial['TargetsTrial'])):
        #Vibration based on which condition 
        try:
            len(thisTrial['Vibration'])>1
            if i%2==0:
                vib = thisTrial['Vibration'][0]
            else: vib = thisTrial['Vibration'][1]
        except: vib = thisTrial['Vibration']
        #Target is set
        Target.setImage(stimpath + thisTrial['VisualTarget'][i])
        #Drawing target on screen
        for frameN in range(targetFrames):
            Target.setAutoDraw(True)
            win.flip()
            
        for frameN in range (isiFrames):
            Target.setAutoDraw(False)
            fixation.setText('')
            fixation.draw()
            win.flip()

            if frameN == gapFrames:
                #Starting vibration after the gap...
                port.setData(vib)
                
            if frameN == vibFrames:
                #Stopping the vibration after 300 (but the duration is only 200 ms!)
                port.setData(0)
            thisTrial['SerialPosition' + str(i+1)] = thisTrial['TargetsTrial'][i]
    #Setting the probe
    Probe.setImage(stimpath + thisTrial['Probe'] + '.bmp') 
    #Retention(?)
    for frameN in range(targetFrames):
            win.flip()
    RTclock.reset()
    thisTrial['Response'] = dispResp()
    thisTrial['RT'] = RTclock.getTime()
    #Check if correct response was made
    if thisTrial['Response'] == thisTrial['CorrectResponse']:
        thisTrial['Accuracy'] = 1
    else:
        thisTrial['Accuracy'] = 0
    #save data for each subject in same file?    
    writeCsv(datafile, thisTrial)
    #Handling blocks
    if trials.getFutureTrial():
        nextTrial = trials.getFutureTrial(n=1) 
    if nextTrial['Block'] != thisTrial['Block']:
        myMouse.setVisible(0)#Hide the mouse during presentation of target digits
        fixation.setText('Take a short break. Press any key on the keyboard to continue')
        fixation.draw()
        win.flip()
        event.clearEvents()
        event.waitKeys()
    if  not trials.getFutureTrial():
       win.flip()
       event.clearEvents()
   

#Save data. Keeping this... saving data for each participant in a sub-folder...
trials.saveAsExcel(fileName=filename, # ...or an xlsx file (which supports sheets)
                  sheetName = 'rawData',
                  stimOut=[], 
                  dataOut=['all_raw'])
                  
fixation.setText('That is the end of the experiment. Thank you for participating')
fixation.draw()
win.flip()
core.wait(4)
event.clearEvents()
win.close()
core.quit()
