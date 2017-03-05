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
        self.n_digits = digits
        self.digits = range(1, digits+1)
        self.trials = nTrials

    def create_trials(self):
        '''Creates a list of trials.
        '''
        trials = []
        for trial_seq in range(self.trials/self.n_digits):
            shuffled = self.digits[:]
            shuffle(shuffled)
            trials.append(shuffled)
        return trials

    def experiment_window(self, color):
        '''For creating the experiment window
        in preferred color
        self.color = color
        '''
        self.win = visual.Window(size=(1920, 1200), fullscr=True, screen=0,
                                 allowGUI=False, allowStencil=False,
            monitor=u'testMonitor', color=color, colorSpace=u'rgb',
            blendMode=u'avg',winType=u'pyglet')
        return self.win

    def create_text_stim(self, win, text, pos, name, height, color):
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
        text_stimulus = visual.TextStim(win=self.win, ori=0, name=self.name,
            text=self.text,    font=u'Arial',
            pos=self.pos, height=self.height,
            color=self.color, colorSpace=u'rgb')
        return text_stimulus

    def present_stim(self, stim, target):
        self.stimulus = stim
        self.target = target
        self.win.flip()
        if self.stimulus == "text":
            self.text_on_screen.setText(target)
            self.text_on_screen.draw()
        elif self.stimulus == "image":
            self.target.draw()
        elif self.stimulus == "sound":
            '''here we will we play the sound
            NOT IMPLEMENTED YET
            '''
            self.target.play()

    def experiment_trials(self, trials, expinfo):
        self.exp = expinfo
        self.trialList = []
        self.correctresp = 'space'

        for trial_seq in trials:
            for trial, digit in enumerate(trial_seq):
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

    def experiment_info(self):
        self.exp_name = u'Sustained Attention'
        self.exp_info = {'Subject Id':'', 'Age':'', 'ExpVersion': 0.4,
                        'Sex': ['Male', 'Female'], 'Task':['SART', 'Vigilance']}
        self.exp_info[u'date'] = data.getDateStr(format="%Y-%m-%d_%H:%M")
        self.infoDlg = gui.DlgFromDict(dictionary=self.exp_info,
                                       title=self.exp_name, fixed=['ExpVersion'])
        self.datafile = u'Data' + os.path.sep + u'DATA_SART.csv'
        if self.infoDlg.OK:
            return self.exp_info
        else:
            return 'Cancelled'

    def run_trials(self, trialObj):
        self.trialhandler = trialObj
        self.timer = core.Clock()
        self.warning_frames = int(self.frameR * .5)
        self.target_frames = int(self.frameR * .25)
        self.iti_frames = int(self.frameR * .9)

        # Warning before experiment start
        for frame in range(self.warning_frames):
            self.present_stim('text', 'Get Ready!')

        for frame in range(self.warning_frames):
            self.present_stim('image', self.mask)

        for trial in self.trialhandler:
            self.timer.reset()
            keys = event.getKeys(keyList=['space'])

            for frame in range(self.target_frames):
                    visualTarget = trial['Stimulus']
                    self.present_stim('text', visualTarget)

            for frame in range(self.iti_frames):
                    self.present_stim('image', self.mask)

                    if keys:
                        trial['RT'] = self.timer.getTime()
                        if keys[0] == trial['Cresp']:
                            trial['Accuracy'] = 1
                        else:
                            trial['Accuracy'] = 0

                        trial['Response'] = keys[0]

                    elif len(keys) == 0:
                        if trial['Cresp'] == 'Noresponse':
                            trial['Accuracy'] = 1
                        else:
                            trial['Accuracy'] = 0

                        trial['Response'] = 'Noresponse'

            trial['RT'] = self.timer.getTime()
            self.write_csv(self.datafile, trial)

    def write_csv(self,fileName, current_trial):
        import codecs, csv, os
        fullpath = os.path.abspath(fileName)
        if not os.path.isfile(fullpath):
            with codecs.open(fullpath, 'ab+', encoding='utf8') as f:
                csv.writer(f, delimiter=';').writerow(current_trial.keys())
                csv.writer(f, delimiter=';').writerow(current_trial.values())
        else:
            with codecs.open(fullpath, 'ab+', encoding='utf8') as f:
                csv.writer(f, delimiter=';').writerow(current_trial.values())

    def create_dir(self, dirname):
        import os
        if not os.path.isdir(dirname):
            os.create_dirs(dirname)

    def run_experiment(self):
        self.create_dir('Data')
        self.expinfo = self.experiment_info()
        if self.expinfo == 'Cancelled':
            print 'User cancelled'
            core.quit()

        self.win = self.experiment_window(color = 'black')
        self.frameR = self.win.getActualFrameRate()
        self.load = Preloading()
        self.files = self.load.load_files("Stimuli", "png", "image", self.win)
        self.txtfiles = self.load.load_files("Stimuli", "txt", "text", self.win)
        self.mask = self.files['circleMask'][0]
        self.text_on_screen = self.create_text_stim(self.win, text='',
                                         pos=[0.0,0.0], name='Visual Target',
                                         height=0.07, color='White')
        self.txtfiles[self.expinfo['Task']].draw()
        self.win.flip()
        event.waitKeys()
        event.clearEvents()
        self.trials = self.create_trials()
        trialsToRun = self.experiment_trials(self.trials, self.expinfo)
        self.run_trials(trialsToRun)
        core.quit()

class Preloading():

    def __init__(self):
        self.path = os.getcwd()

    def load_files(self, directory, extension, filetype, win='', which_files='*', stim_list=[]):
        """ Load all the pics and sounds"""
        self.dir = directory
        self.extension = extension
        self.filetype = filetype
        self.wi = win
        self.which_files = which_files

        if isinstance(self.extension, list):
            file_list = []
            for current_ext in self.ext:
                file_list.extend(glob.glob(
                                        os.path.join(self.path,
                                                       self.directory,
                                                       self.which_files+current_ext)))
        else:
            file_list = glob.glob(os.path.join(self.path,directory, self.which_files+self.extension))
            filematrix = {} #initialize filematrix  as a dict because it'll be accessed by picture names, cound names, whatver
        for num,curFile in enumerate(file_list):
            fullpath = curFile
            fullfilename = os.path.basename(fullpath)
            stimfile = os.path.splitext(fullfilename)[0]

            if filetype == "image":
                from psychopy import visual
                try:
                    surface = pygame.image.load(fullpath) #gets height/width of the image
                    stim = visual.SimpleImageStim(win, image=fullpath)
                    filematrix[stimfile] = ((stim,fullfilename,num,surface.get_width(),surface.get_height(),stimfile))
                except: #no pygame, so don't store the image dims
                    stim = visual.SimpleImageStim(win, image=fullpath)
                    filematrix[stimfile] = ((stim,fullfilename,num,'','',stimfile))

            elif filetype == "sound":
                soundRef = sound.Sound(fullpath)
                filematrix[stimfile] = ((soundRef))
            elif filetype=='text':
                from psychopy import visual
                import codecs
                with codecs.open(fullpath, 'r', encoding='utf8') as f:
                    textRef = visual.TextStim(win, text=f.read(), wrapWidth=1.2, alignHoriz='center', alignVert='center', height=0.06)

                filematrix[stimfile] = ((textRef))

        #check
        if stim_list and set(filematrix.keys()).intersection(stim_list) != set(stim_list):
            popupError(str(set(self.stim_list).difference(filematrix.keys())) + " does not exist in " + self.path+'\\'+directory)

        return filematrix
def main():
    test = Experiment(digits=9, nTrials=225, name="Sustained Attention")
    test.run_experiment()

if __name__ == "__main__":
    main()
