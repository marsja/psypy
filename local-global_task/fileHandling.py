# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 16:32:42 2015

@author: erik
"""
import os, glob, codecs, csv
from psychopy import visual

class fileHandling():
    
    def __init__(self):
        self.path = os.getcwd()
        
    def writeCsv(self,fileName, thisTrial):
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
            fileList = glob.glob(os.path.join(self.path,directory,
                                              self.whichFiles+self.extension))
            fileMatrix = {} #initialize fileMatrix  as a dict because it'll be accessed by picture names, cound names, whatver
        for num,curFile in enumerate(fileList):
            fullPath = curFile
            fullFileName = os.path.basename(fullPath)
            stimFile = os.path.splitext(fullFileName)[0]
            if fileType=="image":
                try:
                    surface = pygame.image.load(fullPath) #gets height/width of the image
                    stim = visual.SimpleImageStim(win, image=fullPath)
                    fileMatrix[stimFile] = ((stim,fullFileName,
                        num,surface.get_width(),surface.get_height(),stimFile))
                except: #no pygame, so don't store the image dims
                    stim = visual.SimpleImageStim(win, image=fullPath)
                    fileMatrix[stimFile] = ((stim,fullFileName,num,'','',stimFile))
            elif fileType=="sound":
                soundRef = sound.Sound(fullPath)
                fileMatrix[stimFile] = ((soundRef))
            elif fileType=='text':
                with codecs.open(fullPath, 'r', encoding='utf8') as f:
                    textRef = visual.TextStim(win, text=f.read(), wrapWidth=1.2, alignHoriz='center', color="Black", alignVert='center', height=0.06)
                
                fileMatrix[stimFile] = ((textRef))

        #check 
        if stimList and set(fileMatrix.keys()).intersection(stimList) != set(stimList):
            popupError(str(set(self.stimList).difference(fileMatrix.keys())) + " does not exist in " + self.path+'\\'+directory)
         
        return fileMatrix

