#Cross-modal oddball experiment
#Erik Marsja, erik at marsja.se (http://www.marsja.se)
#Import the modules needed
import time, os, re, random
from datetime import datetime 
from sgen import trialCreator#My custom made randomzation script

#Psychopy stuff
from psychopy import visual, core, data, event, logging, gui, sound

# Store info about the experiment session
expName = u'Cross-Modal Oddball'  #
expInfo = {u'Participant':'','session':'001'}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
while len(expInfo['Participant']) == 0:
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK == False: core.quit()  # user pressed cancel
#Age and sex ('In Swedish..')
dgr = gui.Dlg(title=u"\u00E5lder och k\u00F6n")
dgr.addField(u'\u00E5lder')
dgr.addField(u'K\u00F6n', choices=['Man', 'Kvinna'])
dgr.show()
if dgr.OK == Fal,
se: core.quit()  # user pressed cancel

#Data file handling
if not os.path.isdir('Data'):
    os.makedirs('Data')  # if this fails (e.g. permissions) we will get error
filename = 'Data' + os.path.sep + 'Data_%s_%s' %(expInfo['Participant'], expInfo['date'])
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

#Respons buttons. Counterbalanced across Ss. 
subid = int(expInfo['Participant'])
if subid%2==0:
    rkeys = {'Odd':'x', 'Even':'z'}
else: rkeys = {'Odd':'z', 'Even':'x'}

#Create window go fullscreen
win = visual.Window(size=(800,600),winType='pyglet',fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1.000,-1.000,-1.000], colorSpace='rgb')
   
 #Experimental instructions (in Swedish)
instrucTxt = u"""Din uppgift  \u00E4r att  avg\u00F6ra om siffran som presenteras p\u00E5 sk\u00E4rmen
\u00E4r udda eller j\u00E4mna. \n
Ignorera eventuella distraktorer (ljud eller vibrationer).
Du ska svara s\u00E5 fort du kan men s\u00E5 t\u00E4tt du kan
Tryck p\u00E5 en tangent for att g\u00E4 vidare.""" 
instrucTxt2=u"""Tryck p\u00E5 %s om siffran  \u00E4r udda
Tryck p\u00E5 %s om siffran  \u00E4r j\u00E4mn
T\u00E4nk  p\u00E5 att trycka s\u00E5 snabbt och r\u00E4tt du kan.

Tryck p\u00E5 en tangent for att starta"""  % (rkeys['Odd'], rkeys['Even'])

paustxt = u"""Du kan nu ta en kort paus \n
Tryck p\u00E5 en tangent for att starta""" 

#Blocks and trials... This is important and needs to be set or else the sgen-script will probably fail...
nBlocks=1
nTrials = 120
#TrialHandling
stmlst = trialCreator(parN=subid, nTrials = nTrials, blocks=nBlocks )#Create and randomize stimuli list
trials = data.TrialHandler(stmlst,1, method="sequential")#Trials are already randomized in the 
trials.data.addDataType('Response')
trials.data.addDataType('Accuracy')#Accuracy
trials.data.addDataType('RT')
trials.data.addDataType('Sound')

#Draw instructions
instr = visual.TextStim(win,text=instrucTxt, alignHoriz="center", alignVert="center", wrapWidth=10)
instr.draw()
win.flip()
event.waitKeys()
event.clearEvents()
instr.setText(instrucTxt2)
instr.draw()
win.flip()
event.waitKeys()
event.clearEvents()

#Experiment settings (durations)
frameR = win.getActualFrameRate() #Gets the framerate of the screen. Used to calculate durations of stim and respwin
print frameR
trialClock = core.Clock()
RT = core.Clock()
respwin= 1.2#Seconds
frameRate =frameR  # Set your screens framerate in Hz
stimDuration = .2  # ms
xDuration = .9 # ms
gDuration =.1 #ms
stimFrames = int(frameRate * stimDuration) #For initial fixation cross and digit stims
blankFrames = int(frameRate * xDuration) #response window
gapFrames = int(frameRate * gDuration)
totalFrames = stimFrames + blankFrames

#starts the experiment
snd='standard.wav'
sound.init(48000,buffer=128)

fixation = visual.TextStim(win , height=.12, units='norm', name="Stim")
avsl = visual.TextStim(win, text='Exp done', height=.12, units='norm')

for thisTrial in trials:
    if thisTrial['Condition'] == "standard":
        snd='standard.wav'
    if thisTrial['Condition']=='deviant':
        snd='novel.wav'
    distract = sound.Sound(snd)
    distract.setVolume(0.8)
    digit = thisTrial['Target']
    cresp = thisTrial['Corr']
    trialClock.reset()
    for frameN in range(stimFrames):#Would be 200 ms on a 60 Hz screen
        fixation.setText('+')
        fixation.draw()
        if frameN == 0:
                distract.play()
        win.flip()
    for frameN in range(gapFrames):
        fixation.setText('+')
        fixation.draw()
        win.flip()
    for frameN in range(stimFrames):
        fixation.setText(digit)
        fixation.draw()
        win.flip()
        if frameN == 0:
            RT.reset()
    for frameN in range (blankFrames):
        fixation.setText('+')
        fixation.draw()
        win.flip()
    keyList = event.getKeys(timeStamped=RT)
    for key in keyList:
            if key in ['escape','q']:
                core.quit()
    if keyList:
        rt = keyList[0][1]
        kep = keyList[0][0]
        if cresp == kep:
            acc = 1
        else: acc = 0
    else:
        rt=0
        acc=0
        kep="No response"
    trials.data.add('RT', rt)
    trials.data.add('Accuracy', acc)
    trials.data.add('Response', kep)
    trials.data.add('Sound', snd)
    print trialClock.getTime()
    if trials.getFutureTrial():
        nextTrial = trials.getFutureTrial(n=1) 
    if nextTrial['Block'] != thisTrial['Block']:
        fixation.setText(paustxt)
        fixation.draw()
        win.flip()
        event.clearEvents()
        event.waitKeys(maxWait=4)
    if  not trials.getFutureTrial():
       avsl.draw()
       win.flip()
       event.clearEvents()
trials.saveAsExcel(fileName=filename, # ...or an xlsx file (which supports sheets)
                  sheetName = 'rawData',
                  stimOut=[], 
                  dataOut=['all_raw'])
win.close()
core.quit()