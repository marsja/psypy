#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, event, core, logging, sound, gui, data, parallel
from trialhandling import writeCsv, makeDir, lsquare, blockOrder, imStim
import os, numpy, random

#Functions
def txtStim(win, text, pos, name, height):
    return visual.TextStim(win=win, ori=0, name=name,
    text=text,    font='Arial',
    pos=pos, height=height, wrapWidth=None,
    color=u'white', colorSpace='rgb',
    depth=-4.0) 
    
def handleKeys(key):
    '''Function for handling keys from the handles and using with
    ratingScale...'''
    
    if key != 191:
        key = str(key)
        event._onPygletKey(symbol=key, modifiers=None, emulated=True)#Buffers the input
        last_state = True # Return true if down
        port.setData(0)
        core.wait(.15)
#Data och fp vars

# Store info about the experiment session
expName = u'Cross-Modality Matching'   #
expInfo = {'FP':'', 'Age':'', 'ExpVersion': 1.0,'Sex': ['Male', 'Female']}
expInfo[u'date'] = data.getDateStr(format="%Y-%m-%d")  # add a simple timestamp
infoDlg = gui.DlgFromDict(dictionary=expInfo, title=expName, fixed=['ExpVersion'])

if infoDlg.OK:
    print expInfo
else: print 'User Cancelled'

#Soundlevels to choose from...
sndlvls = numpy.linspace(0.1, 1.0, 21)
#De startnivÃ¥er. Den fÃ¶rsta listan randomiseras den andra tas baklÃ¤nges
sint = [0.1, 1.0]
vlvl = [5,10,15]
task = ['Attention', 'Attention', 'Attention', 'Intensity', 'Intensity', 'Intensity']#W
snd = 'novel.wav' #fÃ¶r att kunna kÃ¶ra med andra ljud
fpn = int(expInfo['FP'])#Varannan fp far starta med lagsta intensitet pa ljud
trialClock = core.Clock()
#Removed this one...
if fpn%2==0:
    sint.reverse()
    task.reverse()

makeDir('Data')
makeDir('Data\\Subject_files')
filename = u'Data\\Subject_files' + os.path.sep + u'Data_%s_%s' %(expInfo[u'FP'], expInfo[u'date'])
datafile = u'Data' + os.path.sep + u'CM_-_Matching_sound_intensit_vs_vibration.csv'

#Skapar fÃ¶nstret fÃ¶r experimentet
win = visual.Window(size=(1920, 1200), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor=u'testMonitor', color=[0,0,0], colorSpace=u'rgb',
    blendMode=u'avg',winType='pyglet')

expInfo[u'frameRate']=win.getActualFrameRate()
#Input --- Mouse + handtagen just nu
port = parallel.ParallelPort(address=0x1120) #For output
inp = parallel.ParallelPort(address=0x1121) #For input from handles, gulmarkerade = 63, svartmarkerade = 255

#Instruktioner
instruk = u"""Uppgiften är att matcha ljudintensiteten (volymen) i ett ljud med intensiteten hos vibrationer. Detta kommer du göra 12 gånger
 för varje ljud- och vibrationskombination. 
Du ska ställa in ljudets volym så att du upplever att ljudintensiteten  matchar vibrationens intensitet. \n\n
Till exempel, om du tycker att ljudets volym ska vara högre justerar du det så att volymem blir högre (genom att trycka på knappen på handtaget i din högra hand). \n
Ta handtagen i dina h\u00E4nder,\n
Tryck p\u00E5 en knapp p\u00E5 n\u00E5got av handtagen för att starta uppgiften"""

ainstruk = u'''Uppgiften är att matcha ljudvolymen så att du upplever att ljudet fångar din uppmärksamheten lika mycket som vibrationen. Detta kommer du göra 12 gånger för varje ljud- och vibrations kombination.
Du ska ställa in ljudets volym så att du upplever att det fångar din uppmärksamhet i samma grad som vibrationen.
Ta handtagen i dina händer.\n
Tryck på en knapp på något av handtagen för att starta uppgiften'''

avsl = u"Nu \u00E4r experimentet klart. Tack f\u00F6r ditt deltagande!"
instruk1 = u'''Ställ in ljudet så att du upplever att det fångar din uppmärksamhet i samma grad som vibrationen. \n\nTryck på knappen på det vänstra handtaget för att sänka volymen, tryck på knappen på det högra handtaget för att höja volymen.\nTryck enter för att svara.'''
instruk2 = u'''Ställ in ljudet så att du upplever att det har samma intensitet som vibrationen.  \n\n
Tryck på knappen på det vänstra handtaget för att sänka volymen, tryck på knappen på det högra handtaget för att höja volymen.\nTryck enter för att svara.'''
txtOnScreen = txtStim(win, text='+', pos=[0.0,0.0], height= 0.05, name=u'Text Object on Screen')
txtOntrial = txtStim(win, text=instruk2, pos=[0.0,0.3], height= 0.05, name=u'Trial')
#FÃ¶r responsknapparna att styra ljud och vibrationer med
myItem = visual.TextStim(win, text=None, pos=[0.0,0.8], name=u'Trial Text')
#Practice image
pracTarget =  imStim(win=win, image='image1.png', pos=[0.0,0.0], name='TargetPractice')
practiceTxt = u'''Du kommer nu få göra en övningsuppgift: matcha ljudintensiteten (volymen) i ett ljud med intensiteten i bilder som visas på skärmen. Detta kommer du göra 6 gånger för varje ljud- och bildkombination. 
Du ska ställa in ljudets volym så att du upplever att ljudintensiteten  matchar bildens intensitet. \n\n
Till exempel, om du tycker att bildens intensitet är större än ljudet så ökar du ljudets intensitet genom att trycka på höger knapp. Tycker du intensiteten hos bilden är lägre trycker du på den vänstra knappen.\n
Tryck på någon knapp på handtagen för att starta övningsuppgiften'''
myPrac = visual.TextStim(win, text=instruk2, pos=[0.0,0.5], height= 0.05, name=u'Trial Text')
#Durations
vibFrames = int(expInfo['frameRate'] * 0.2)
delayFrames = int(expInfo['frameRate'] * 1.0)

event.clearEvents()


trialClock.reset()

#What blockorder? Using latin square design
#First a square design is done with the function. We have 3 conditions (cCount = 3!)
squares= lsquare(cCount=3) 

#Determining the order. Need to pass the square design, num of Partcipants and the current participant number
#Returns a list with 0,1,2 (0=baseline, 1=steady state, 2=changing state)
order = blockOrder(skv=squares, nParticipants=42, participant=int(expInfo['FP']))

#Practice 
targ = 0
stimList=[]
pracTargets = ['image1.png','image2.png']
for i in range(2):
    if i == 0: targ = 0
    else: targ = 1
    for trial in range(1,7):
        if trial <= 3:
            stimList.append( 
                {'Startlvl':sint[0], 'Trial':trial, 'Visual':pracTargets[targ]})
        else: 
            stimList.append( 
                {'Startlvl':sint[1], 'Trial':trial, 'Visual':pracTargets[targ]})
practice = data.TrialHandler(stimList,1, method="sequential")

#Experiment trialhandling...
stimList=[]
expTrial = 0
idx = [0,1,2,0,1,2]
for i in range(0,6):
    block = i+1
    for trial in range(1,13):
        expTrial += 1
        if trial <= 6:
            stimList.append( 
                {'Startlvl':sint[0], 'Trial':trial, 'Block':block,'Vib':vlvl[idx[i]], 'VibOrder':order, 'Task':task[i], 'ExpTrial':expTrial,
                'Sub_id':fpn, 'Age':expInfo['Age'], 'Sex':expInfo['Sex']} )
        else: 
            stimList.append( 
                {'Startlvl':sint[1], 'Trial':trial, 'Block':block, 'Vib':vlvl[idx[i]],'VibOrder':order, 'Task':task[i], 'ExpTrial':expTrial,
                'Sub_id':fpn, 'Age':expInfo['Age'], 'Sex':expInfo['Sex']} )

trials = data.TrialHandler(stimList,1, method="sequential")
trials.data.addDataType('Volume')
trials.data.addDataType('Response')

#Instruktions text practice
pracnotClicked = True
while pracnotClicked:  
    hInp = inp.readData()
    if hInp == 63 or hInp == 255:
        pracnotClicked = False
    txtOnScreen.setText(practiceTxt)
    txtOnScreen.draw()
    win.flip()
txtOnScreen.setText('+')
txtOnScreen.draw()
win.flip()
last_state = False #Buttons not pressed

timingClock = core.Clock()
for thisTrial in practice:
    #Bestam vart den ska starta
    if  thisTrial['Startlvl'] == 0.1:
        mStart = 0 # starta frÃ¥n lÃ¥g eller hÃ¶g
    else:
        mStart = 20
    tada = sound.Sound(snd)
    tx = u"St\u00E4ll in ljudintensitet: " + str(thisTrial['Trial']) 
    pracTarget.setImage(thisTrial['Visual'])
    myItem.setText(tx)
    txtOnScreen.setText(instruk2)
    #Starta varje trial med att spela och vibrera
    for i in range(vibFrames):
        txtOnScreen.setText('+')
        txtOnScreen.draw()
        win.flip()
        if i == 0:
            if mStart == 21:
                tada.setVolume(sndlvls[20])
            else: tada.setVolume(sndlvls[mStart])
            tada.play()
    event.clearEvents()
    myRatingScale = visual.RatingScale(win, noMouse=True, markerStart=mStart, marker="slider",acceptText='Tryck enter', acceptPreText='Tryck knapp',  \
    pos=[0.0,-0.6], textSize=0.5, high=20, low=0, leftKeys='255',rightKeys='63',scale=None, labels=['Lower', 'Higher'],tickMarks=[0,20], showValue=False)
    timingClock.reset()

    while myRatingScale.noResponse: # show & update until a response has been made
        t = timingClock.getTime()
        for key in event.getKeys():
            if key in ['escape','q']:
                core.quit()
        if not last_state:
            hInp = inp.readData()
            last_state = handleKeys(hInp)
        myPrac.draw()
        myItem.draw()
        pracTarget.draw()
        myRatingScale.draw()
        if myRatingScale.getRating()==21: fv = sndlvls[20]
        else: fv = sndlvls[myRatingScale.getRating()]
     
        if isinstance(fv, float): #Kan vara Ã¶verflÃ¶digt
            tada.setVolume(fv)   
        else:
            tada.setVolume(fv)

        if t>=0.798 and t<=0.804:
            tada.setVolume(fv)
            tada.play()
        if t>1.6:
            timingClock.reset()
        win.flip()
            
    for i in range(delayFrames):
        if i == 0:
            txtOnScreen.setText('+')
            txtOnScreen.draw()
            win.flip()
    if  not trials.getFutureTrial():
       txtOnScreen.setText(avsl)
       txtOnScreen.draw()
       win.flip()
       event.clearEvents()
#Instruktions text experiment
if task[0]=='Attention':instructions = ainstruk
else: instructions = instruk
notClicked = True
while notClicked:  
    hInp = inp.readData()
    if hInp == 63 or hInp == 255:
        notClicked = False
    txtOnScreen.setText(instructions)
    txtOnScreen.draw()
    win.flip()
txtOnScreen.setText('+')
txtOnScreen.draw()
win.flip()

#Startar experimentet
for thisTrial in trials:
    #Bestam vart den ska starta
    if  thisTrial['Startlvl'] == 0.1: mStart = random.randint(0,4) #Start in the lower end
    else: mStart = random.randint(17,21)#start in the higher end
    if  thisTrial['Task'] == 'Attention': scrinstruc = instruk1
    else: 
        scrinstruc = instruk2
    tada = sound.Sound(snd)
    tx = u"St\u00E4ll in ljudet: " + str(thisTrial['Trial']) + u' Block: ' + str(thisTrial['Block']) 
    vb = thisTrial['Vib']
    txtOntrial.setText(scrinstruc)
    myItem.setText(tx)
    #Starta varje trial med att spela och vibrera
    for i in range(vibFrames):
        txtOnScreen.setText('+')
        txtOnScreen.draw()
        win.flip()
        if i == 0:
            if mStart == 21: tada.setVolume(sndlvls[20])
            else: tada.setVolume(sndlvls[mStart])
            tada.play()
        if i == vibFrames-1:
            port.setData(0)
    event.clearEvents()
    core.wait(1)
    myRatingScale = visual.RatingScale(win, noMouse=True, markerStart=mStart, marker="slider",acceptText='Tryck enter', acceptPreText='Tryck knapp',  \
    pos=[0.0,0.0], textSize=0.5, high=20, low=0, leftKeys='255',rightKeys='63',scale=None, labels=['Lower', 'Higher'],tickMarks=[0,20], showValue=False)
    timingClock.reset()

    while myRatingScale.noResponse: # show & update until a response has been made
        t = timingClock.getTime()
        for key in event.getKeys():
            if key in ['escape','q']:
                core.quit()
        if not last_state:
            hInp = inp.readData()
            last_state = handleKeys(hInp)
        txtOntrial.draw()
        myItem.draw()
        myRatingScale.draw()
        if myRatingScale.getRating()==21: fv = sndlvls[20]
        else: fv = sndlvls[myRatingScale.getRating()]

        if isinstance(fv, float): #Kan vara Ã¶verflÃ¶digt
            tada.setVolume(fv)   
        else:
            tada.setVolume(fv)

        if t>=0.798 and t<=0.804:
            port.setData(vb)
            tada.setVolume(fv)
            tada.play()
        if t>=0.998 and t<=1.04:
             port.setData(0)
        if t>1.6:
            timingClock.reset()

        win.flip()
            
        rating = myRatingScale.getRating() # get the value indicated by the subject, 'None' if skipped
    port.setData(0)
    thisTrial['Response'] = rating
    thisTrial['Volym'] = fv    
    writeCsv(datafile, thisTrial)
    for i in range(delayFrames):
        if i == 0:
            txtOnScreen.setText('+')
            txtOnScreen.draw()
        win.flip()
        #Handling blocks
    if trials.getFutureTrial():
        nextTrial = trials.getFutureTrial(n=1) 
    if nextTrial['Task'] != thisTrial['Task']:
        if nextTrial['Task'] == 'Attention':instructions=ainstruk
        else:instructions=instruk
        notClicked = True
        while notClicked:  
            hInp = inp.readData()
            if hInp == 63 or hInp == 255:
                notClicked = False
            txtOnScreen.setText(instructions)
            txtOnScreen.draw()
            win.flip()
    if  not trials.getFutureTrial():
       txtOnScreen.setText(avsl)
       txtOnScreen.draw()
       win.flip()
       event.clearEvents()
       event.waitKeys(maxWait=5)

print trialClock.getTime()/60
#Spara
trials.saveAsExcel(fileName=filename, # ...or an xlsx file (which supports sheets)
                  sheetName = 'rawData',
                  stimOut=['Trial', 'Block', 'Startlvl', 'Vib'], 
                  dataOut=['Level_raw', 'Volym_raw'], appendFile=False)
win.close()
core.quit()
