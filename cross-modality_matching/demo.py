#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, event, core, logging, sound, gui, data
#Importing some functions to take care of latin square design, write data file, and so on... (See file trialhandling.py)
from trialhandling import writeCsv, makeDir, lsquare, blockOrder, imStim
import os, numpy, random

#Functions
def txtStim(win, text, pos, name, height):
    ''''Saving a few lines of code. Creating text stimuli'''
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

# Store info about the experiment session
expName = u'Cross-Modality Matching'   #
expInfo = {'Subject_Id':'', 'Age':'', 'ExpVersion': 2.0,'Sex': ['Male', 'Female']}
expInfo[u'date'] = data.getDateStr(format="%Y-%m-%d_%H:%M")  # add a simple timestamp
infoDlg = gui.DlgFromDict(dictionary=expInfo, title=expName, fixed=['ExpVersion'])

if infoDlg.OK:
    print expInfo
else: print 'User Cancelled'

#Soundlevels to choose from...
sndlvls = numpy.linspace(0.1, 1.0, 21)
#List of sound levels to start from
sint = [0.1, 1.0]
#List of vibration intensities
vlvl = [5,5,5,5,10,10,10,10,15,15,15,15]
#List of the tasks
task = ['Attention', 'Attention', 'Attention', 'Intensity', 'Intensity', 'Intensity']
#Sound
snd = 'novel.wav'

#Sub_id. 50 % start in the lower end of sound level..
fpn = int(expInfo['Subject_Id'])
expClock = core.Clock()

#Counterbalancing which hand vibrations will start... 
if fpn%2==0:
    task.reverse()

#Making data dir using my function
makeDir('Data')
makeDir('Data\\Subject_files')
filename = u'Data\\Subject_files' + os.path.sep + u'Data_%s_%s' %(expInfo[u'Subject_Id'], expInfo[u'date'])
datafile = u'Data' + os.path.sep + u'CM_-_Matching_snd_n_vib.csv'
timefile = u'Data' + os.path.sep + u'timeittook.csv'

#Creates window for the experiment
win = visual.Window(size=(1920, 1200), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor=u'testMonitor', color=[0,0,0], colorSpace=u'rgb',
    blendMode=u'avg',winType='pyglet')

expInfo[u'frameRate']=win.getActualFrameRate()
#Input --- Mouse + handtagen just nu
port = parallel.ParallelPort(address=0x1120) #For output
inp = parallel.ParallelPort(address=0x1121) #For input from handles, gulmarkerade = 63, svartmarkerade = 255

#Instructions
instruk = u"""Din uppgift är att matcha intensiteten (volymen) i ett ljud med intensiteten hos vibrationer. Detta kommer du göra 12 gånger
 för varje ljud- och vibrationskombination. 
Du ska ställa in ljudets volym så att du upplever att ljudintensiteten  matchar vibrationens intensitet. \n\n
Till exempel, om du tycker att ljudets volym ska vara högre justerar du det så att volymem blir högre (genom att trycka på knappen på handtaget i din högra hand). \n
Ta handtagen i dina händer,\n
Tryck på en knapp på något av handtagen för att starta uppgiften"""

ainstruk = u'''Uppgiften är att matcha ljudvolymen så att du upplever att ljudet fångar din uppmärksamheten lika mycket som vibrationen. Detta kommer du göra 12 gånger för varje ljud- och vibrations kombination.
Du ska ställa in ljudets volym så att du upplever att det fångar din uppmärksamhet i samma grad som vibrationen.
Ta handtagen i dina händer.\n
Tryck på en knapp på något av handtagen för att starta uppgiften'''

avsl = u'''Nu är experimentet klart. Tack för ditt deltagande!'''
#Instructions attention capture dimension
instruk1 = u'''Ställ in ljudet så att du upplever att det fångar din uppmärksamhet i samma grad som vibrationen. \n\nTryck på knappen på det vänstra handtaget för att sänka volymen, tryck på knappen på det högra handtaget för att höja volymen.\nTryck enter för att svara.'''
#Intensity instructions
instruk2 = u'''Ställ in ljudet så att du upplever att det har samma intensitet som vibrationen.  \n\n
Tryck på knappen på det vänstra handtaget för att sänka volymen, tryck på knappen på det högra handtaget för att höja volymen.\nTryck enter för att svara.'''
#Create some textobjects
txtOnScreen = txtStim(win, text='+', pos=[0.0,0.0], height= 0.05, name=u'Text Object on Screen')
txtOntrial = txtStim(win, text=instruk2, pos=[0.0,0.3], height= 0.05, name=u'Trial')
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

expClock.reset()

targ = 0
stimList=[]
pracTargets = ['image1.png','image2.png']
for i in range(2):
    if i == 0: targ = 0
    else: targ = 1
    for trial in range(1,7):
        idx = random.randint(0,20)
        if trial <= 3:
            stimList.append( 
                {'Startlvl':sndlvls[idx], 'Trial':trial, 'Visual':pracTargets[targ]})
        else: 
            stimList.append( 
                {'Startlvl':sndlvls[idx], 'Trial':trial, 'Visual':pracTargets[targ]})
practice = data.TrialHandler(stimList,1, method="sequential")

#Experiment trialhandling...
stimList=[]
expTrial = 0
#Indices to be used in the following loop. Getting right sound levels...

for i in range(0,6):
    #Looping through 6 blocks
    block = i+1
    #Randomize the vibrations
    random.shuffle(vlvl)
    #Each block containts 12 trials
    for trial in range(0,12):
        
        #Random number to choose soundstart level from;
        idx = random.randint(0,20)
        expTrial += 1
        #Half of the trials will start from one end of the sound level...
        if trial <= 6:
            #Creating a list containing dictionaries. Each dictionary is a trial. 
            stimList.append( 
                {'Startlvl':sndlvls[idx], 'Trial':trial, 'Block':block,'Vib':vlvl[trial], 'Task':task[i], 'ExpTrial':expTrial,
                'Sub_id':fpn, 'Age':expInfo['Age'], 'Sex':expInfo['Sex'], 'Date':expInfo['date']} )
         #The other half start from the other end...
        else: 
            stimList.append( 
                {'Startlvl':sndlvls[idx], 'Trial':trial, 'Block':block, 'Vib':vlvl[trial], 'Task':task[i], 'ExpTrial':expTrial,
                'Sub_id':fpn, 'Age':expInfo['Age'], 'Sex':expInfo['Sex'], 'Date':expInfo['date']} )


#Using Trialhandler to create the object to be run as experiment later...
trials = data.TrialHandler(stimList,1, method="sequential")
#Adding stuff to that...
trials.data.addDataType('Volume')
trials.data.addDataType('Response')
trials.data.addDataType('TrialTime')


#Instructions text practice
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
last_state = False #Reset button press...

#Just a clock to time stuff... 
timingClock = core.Clock()
trialClock = core.Clock()
for thisTrial in practice:
    #So where on the ratingScale used are the ticker gonna start?
    mStart = numpy.argmax(sndlvls==thisTrial['Startlvl'])
    #Creating sound object
    tada = sound.Sound(snd)
    #Changing text to be on screen
    tx = u"Ställ in ljudintensitet: " + str(thisTrial['Trial']) 
    #Setting the image stored in the dictionary thisTrial (which is in trials, created by trialhandler...)
    pracTarget.setImage(thisTrial['Visual'])
    myItem.setText(tx)
    txtOnScreen.setText(instruk2)
    for i in range(vibFrames):
        txtOnScreen.setText('+')
        txtOnScreen.draw()
        win.flip()
        if i == 0:
            tada.setVolume(sndlvls[mStart])
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
        fv = sndlvls[myRatingScale.getRating()]
     
        if isinstance(fv, float): 
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
#Instructions for experiment
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

#The test part of the experiment starts hear...
for thisTrial in trials:
    #Reset the clock
    trialClock.reset()
    #Where is it gonna be started (the ticker...)
    mStart = numpy.argmax(sndlvls==thisTrial['Startlvl']) 
    if  thisTrial['Task'] == 'Attention': scrinstruc = instruk1
    else: 
        scrinstruc = instruk2
    tada = sound.Sound(snd)
    tx = u"St\u00E4ll in ljudet: " + str(thisTrial['Trial']) + u' Block: ' + str(thisTrial['Block']) 
    vb = thisTrial['Vib']
    txtOntrial.setText(scrinstruc)
    myItem.setText(tx)
    #Starting a trial...
    for i in range(vibFrames):
        txtOnScreen.setText('+')
        txtOnScreen.draw()
        win.flip()
        if i == 0:
            tada.setVolume(sndlvls[mStart])
            port.setData(vb)
            tada.play()
        if i == vibFrames-1:
            port.setData(0)
    event.clearEvents()
    core.wait(1)
    myRatingScale = visual.RatingScale(win, noMouse=True, markerStart=mStart, marker="slider",acceptText='Tryck enter', acceptPreText='Tryck knapp',  \
    pos=[0.0,0.0], textSize=0.5, high=20, low=0, leftKeys='255',rightKeys='63',scale=None, labels=['Lower', 'Higher'],tickMarks=[0,20], showValue=False)
    timingClock.reset()

    while myRatingScale.noResponse: # show & update until a response has been made
        #Timing so that vibration will be approx 200 ms
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

        if isinstance(fv, float): 
            tada.setVolume(fv)   
        else:
            tada.setVolume(fv)
        #Well the timer will never be exact so when its here play sound and vibrate
        if t>=0.798 and t<=0.804:
            port.setData(vb)
            tada.setVolume(fv)
            tada.play()
         #same as above but stop the vibration... gives an approx 200 ms vib...
        if t>=0.998 and t<=1.04:
             port.setData(0)
        if t>1.6:
            #Yes reset the clock....
            timingClock.reset()
        win.flip()

        rating = myRatingScale.getRating() # get the value indicated by the subject, 'None' if skipped
    port.setData(0)
    #Collect the responses from the rating scale... 
    thisTrial['Response'] = rating
    #Which volume was played?
    thisTrial['Volume'] = fv    
    #How long did it take?
    thisTrial['TrialTime'] =  trialClock.getTime()
    #Save trial to row in csv-file
    writeCsv(datafile, thisTrial)
    for i in range(delayFrames):
        if i == 0:
            txtOnScreen.setText('+')
            txtOnScreen.draw()
        win.flip()
    #iF there is a next trial store it
    if trials.getFutureTrial():
        nextTrial = trials.getFutureTrial(n=1) 
     #If next trial is not the same as the current new instructions for the new task is printed....
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

print expClock.getTime()/60
#Writing a file with each partipants time to complete the task;
timeDic = {'Sub_id':fpn,'ExpTime':expClock.getTime()/60}
writeCsv(timefile, timeDic)

win.close()
core.quit()
