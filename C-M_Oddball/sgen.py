import random, re
#Function for applying standard and deviants to a list. In this list no randomization is done.
def expSetup(subid, rkeys, digits, block):
    dlist = []
    templist = []
    trialN=0
    for i in range(len(digits)):
        tmp = 0
        for b in range(1,16): #For 120 trials make the number of digits even
            trialN +=1
            if tmp <= 2:#
                cond="deviant"
                tmp += 1
            else: cond="standard"
            #Setting correct responses and everything else. Each trial is one dict in the list
            if i%2==0:
                templist.append({'Sub_id':subid,'Trial':0, 'Block':block+1, 'Condition':cond,'Corr':rkeys['Even'],'Target':digits[i]})
            else: 
                templist.append({'Sub_id':subid,'Trial':0, 'Block':block+1, 'Condition':cond,'Corr':rkeys['Odd'],'Target':digits[i]})
        dlist = templist
    return dlist

def swap(a, i, j):
    '''swap items i and j in the list a'''
    a[i], a[j] = a[j], a[i]
def moveNovel(ind, nT, trials):
    for a in range(nT):
        s = random.randint(0,nT-2)
        try:    
                prev1 = trials[s-1]["Condition"]
                prev2 = trials[s-2]["Condition"]
                nex1 =  trials[s+1]["Condition"]
                nex2 = trials[s+2]["Condition"]
                '''Checks if index is surrounded by "Standards"...
                Move the novel if that is the case. Added the last and () to have 2 standards'''
                if mObS.match(trials[s]["Condition"]) and ((mObS.match(prev1)and mObS.match(nex1)) \
                and (mObS.match(prev2)and mObS.match(nex2))):
                    c = s
                    swap(trials, ind, c)
        except IndexError:
            continue
   
def randomizeStim(trials, nT):#trials = list of trials dicts.. nT = number of trials
#Randomize the list
#Trials = the list of trials made with expSetup. A list of dicts...
    random.shuffle(trials)
#make sure there are not two consequitive deviants
    for i in range(nT):
        if mObD.match(trials[i]["Condition"]) and (i == 0 or i == 119):
            b = i
            moveNovel(b, nT, trials)
        try:#Checking indexes surrounding trial i
            prev = trials[i-1]["Condition"]
            prev2 = trials[i-2]["Condition"]
            nex1 = trials[i+1]["Condition"]
            nex2 = trials[i+2]["Condition"]
            if mObD.match(trials[i]["Condition"]) and ((mObD.match(prev) or mObD.match(nex1)) \
            or (mObD.match(prev) and mObD.match(nex1)) or (mObD.match(prev2) or mObD.match(nex2))):
                b = i
                moveNovel(b, nT, trials)
            #Added to have at least 2 standards between devs
        except IndexError:
            continue
        '''Not the first and the last in each block is a novel. Might not be a problem after all...'''            
    return trials

"Regexp for matching different novels"
mObD = re.compile(r'deviant\W*\d*')
mObS = re.compile(r'standard\W*\d*')
def trialCreator(parN, nTrials, blocks):
    '''Starting with counterbalencing the response buttions
    even participant numbers get 'x' as odd and 'z' as even'''
    if parN%2==0: rkeys = {'Odd':'x', 'Even':'z'}
    else: rkeys = {'Odd':'z', 'Even':'x'}
    #creates list of digits to be used
    digits=[]
    for i in range(1,9):
        digits.append(str(i))
    subid=parN
    bTrials = nTrials/blocks #How many trials/block?
    templ = []
    for i in range(blocks):
        digList=expSetup(subid, rkeys, digits, i)
        stims = randomizeStim(digList, bTrials)
        for trialN in range(len(stims)):
            stims[trialN]['Trial'] = trialN+1
        templ = templ + stims
    return templ
if __name__ == "__main__":
    tr = trialCreator(parN=1, nTrials = 720, blocks= 6) #Gets a list of trials for all blocks

