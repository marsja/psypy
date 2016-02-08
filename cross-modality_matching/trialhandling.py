# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 11:15:58 2015

@author: erkmaa04
"""

def makeDir(dirname):
    import os
    if not os.path.isdir(dirname):
        os.makedirs(dirname)  # if this fails (e.g. permissions) we will get error

def writeCsv(fileName, thisTrial):
    import codecs, csv, os
    fullPath = os.path.abspath(fileName)
    if not os.path.isfile(fullPath): 
        with codecs.open(fullPath, 'ab+', encoding='utf8') as f:
                csv.writer(f, delimiter=';').writerow(thisTrial.keys())
                csv.writer(f, delimiter=';').writerow(thisTrial.values())
    else:
        with codecs.open(fullPath, 'ab+', encoding='utf8') as f:
                csv.writer(f, delimiter=';').writerow(thisTrial.values())
   
  
def imStim(win, image, pos, name):
    from psychopy import visual
    return visual.ImageStim(win=win, name=name,
        image=image, mask=None,
        ori=0, pos=pos,
        colorSpace=u'rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=-5.0)



def shuffleACopy(x):
    import random
    b = x[:] # make a copy of the keys
    random.shuffle(b) # shuffle the copy
    return b # return the copy
        
def blockOrder(skv, nParticipants, participant):
    # write to file for each participant,
    numberofParticipants = nParticipants
    nPartList = range(1,numberofParticipants+1)
    
    for i in range(1,numberofParticipants):
        if participant in nPartList[0::6]:
              write_square = skv[0]
        elif participant in nPartList[1::6]:
              write_square = skv[1]    
        elif participant in nPartList[2::6]:
              write_square = skv[2]   
        elif participant in nPartList[3::6]:
              write_square = skv[3]    
        elif participant in nPartList[4::6]:
              write_square = skv[4] 
        elif participant in nPartList[5::6]:
              write_square = skv[5]   
        return write_square

def lsquare(cCount):
  import copy  
  # input
  conditionCount = cCount
  # first line
  firstLine = [0, 1]
  useBack = True
  choices = range(2, conditionCount)
  for i in range(2, conditionCount):
    if useBack:
      number = choices.pop()
    else:
      number = choices.pop(0)
    firstLine.append(number)
    useBack = not useBack
    
  # Latin square
  square = [firstLine]
  for i in range (1, conditionCount):
    line = [(element + i) % conditionCount for element in firstLine]
    square.append(line)
  
  # add reversed lines Latin square for odd-numbered condition
  if (conditionCount % 2 != 0):
   reversedSquare = []
   for line in square:
     reversedLine = copy.copy(line)
     reversedLine.reverse()
     reversedSquare.append(reversedLine)
   square.extend(reversedSquare)
   
  # output
  sqr = []
  for line in square:
    sqr.append(line)
  return sqr

def genTrials(nTrials):
    from random import shuffle, randint
    idx = randint(0,9)
    digits = range(0,10)
    digits.pop(idx)
    retList = [shuffleACopy(digits) for x in range(nTrials)]

    return retList
    

def genProbes(trials):
    '''Each position need to be equally probed'''
    from random import randint as rand
    numberOfprobes = len(trials)/8 #To get how many probes/serial position
    
    #create a dict with the probes to keep count
    probes = {}
    probeList = [] #to store each trials probe...
    for i in range(8):
        probes[i]=0

    for i in range(len(trials)):
 
        serialposition = rand(0,7)#getting an index to randomly 
        while probes[serialposition] == numberOfprobes:
            serialposition = rand(0,7)
          
        probeList.append(serialposition)
        probes[serialposition] += 1
  
    return probeList
    
#test = lsquare(cCount=3)
#for i in range(1,7):
#    order = blockOrder(skv=test, nParticipants=42, participant=i)
#    print order
