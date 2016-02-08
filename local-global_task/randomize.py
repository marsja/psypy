# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 14:38:26 2015

@author: erik
"""
from random import shuffle
from collections import Counter

liststim = []
colors, firstfigures = ['Black', 'Blue'], ['Rect', 'Triangle', 'X', 'Circle']
secondfigures = firstfigures
for col in colors:
    for figure in firstfigures:
        for figure2 in secondfigures:
            liststim.append(col + '-' + figure + '_' + figure2)

def wasRandomizationSuccessful(trialTypes, ntrials):
    randomizationWorked = False
    #Frequency of the trialtypes
    freq = Counter(trialTypes).values()
    if freq[0] == freq[1] and sum(freq) == ntrials:
        randomizationWorked = True
    return randomizationWorked

class randomizeTrials():
    def __init__(self,nTrials, targets):
        self.nTrials = nTrials
        self.targets = targets
        
    def checkNofTypes(self, countOfTargets, toCheck):
        if countOfTargets <= toCheck:
            return True
        else: 
            return False
            
    def wasRandomizationSuccessful(self,trialTypes):
        randomizationWorked = False
        #Frequency of the trialtypes
        freq = Counter(trialTypes).values()
        if freq[0] == freq[1] and sum(freq) == self.nTrials:
            randomizationWorked = True
        return randomizationWorked

            
    def randomize(self):
        nEachstim = self.nTrials/len(self.targets) 
        stimList = self.targets 
        trialTypes = [] 
        stims = []
        countOfStim = dict((el,0) for el in stimList)
        count = {'ns':0,'s':0}
        for i in range(self.nTrials):
            shuffle(stimList)
            for idx in range(len(stimList)):
                if not stims:
                    countOfStim[stimList[idx]] +=1
                    stims.append(stimList[idx])
                    count['ns'] +=1
                    trialTypes.append("No-Shifting")
                elif stims:
                    if self.checkNofTypes(count['s'], self.nTrials/2):
                        if self.checkNofTypes(countOfStim[stimList[idx]], nEachstim-1):
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
                    elif count['s'] > self.nTrials/2:
                        if countOfStim[stimList[idx]] <= nEachstim-1: 
                            if stimList[idx][:5] == stims[i-1][:5]:
                                count['ns'] +=1
                                countOfStim[stimList[idx]] +=1
                                stims.append(stimList[idx])
                                trialTypes.append("No-Shifting")
    
        if self.wasRandomizationSuccessful(trialTypes):
            return stims
        else:
            return randShift(stimList, self.nTrials)        
        
        
def randShift(listostim, ntrials):
    '''
    Will randomize 50 % of shifting trials
    based on that each filename (of the images) starts with Black or Blue-.
    
    listostim is a list of trials
    ntrials is an integer indicating number of trials
    '''
    nEachstim = ntrials/len(liststim) #Number of each stim is going to be even
    stimList = listostim 
    trialTypes = [] 
    stims = []
    countOfStim = dict((el,0) for el in stimList)
    count = {'ns':0,'s':0}
    for i in range(ntrials):
        shuffle(stimList)
        for idx in range(len(stimList)):
            if not stims:
                countOfStim[stimList[idx]] +=1
                stims.append(stimList[idx])
                count['ns'] +=1
                trialTypes.append("No-Shifting")
            elif stims:
                if count['s'] <= ntrials/2:
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
                elif count['s'] > ntrials/2:
                    if countOfStim[stimList[idx]] <= nEachstim-1: 
                        if stimList[idx][:5] == stims[i-1][:5]:
                            count['ns'] +=1
                            countOfStim[stimList[idx]] +=1
                            stims.append(stimList[idx])
                            trialTypes.append("No-Shifting")

    if wasRandomizationSuccessful(trialTypes, ntrials):
        return stims
    else:
        return randShift(stimList, ntrials)

randomized = randShift(liststim, 96)

rand = randomizeTrials(96, liststim)