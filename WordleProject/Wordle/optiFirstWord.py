from Wordle import *
from multiprocessing import Process, Queue
from os import chdir, getcwd
from sys import stdout
from time import time
from random import randint
import numpy as np

chdir(getcwd()+"\DB")

DBrated = open('Choice1', 'r', encoding="utf8")
strDB = [e.strip()[:-1].lower() for e in DBrated.readlines()]
évalDB = [(float(string[6:]), string[:5]) for string in strDB]
évalDB.sort()

choice2 = open('TARIEchoice2', 'r', encoding="utf8")
dicopatern = {e[:5]:e[6:-1] for e in choice2.readlines()}
Listchoice2 = [(e[:5], e[6:-1]) for e in choice2.readlines()]


def evalPatern(toGuess, mot):
    taillemot = len(mot)
    patern = ''
    vertes, oranges = '', []
    for i in range(taillemot):
        l = mot[i]
        if l == toGuess[i]:
            patern+='🟩'
            vertes+=l
        elif l not in toGuess:
            patern+='🟥'
        else:
            patern+='🟨'
            oranges.append((l,i))

    letavailable = {}
    for e in toGuess:
        letavailable[e] = letavailable[e] + 1 if e in letavailable else 1

    for l in vertes:
        letavailable[l] -= 1

    for (l, i) in oranges:  # on souhaite éliminer les faux oranges
        if letavailable[l] <= 0:
            patern = patern[:i]+'🟥'+patern[i+1:]
        letavailable[l] -= 1
    return patern

def matchInList(patmot, patern):
    rouge,vert,orange = [],[],[]
    for i in range(len(patern)):
        sym = patern[i]
        if sym == '🟩':
            vert.append((patmot[i], i))
        if sym == '🟥':
            rouge.append((patmot[i], i))
        if sym == '🟨':
            orange.append((patmot[i], i))

    let_connu = {}
    for (l,_) in orange + vert:
        let_connu[l] = 1 if l not in let_connu else let_connu[l] + 1

    DBclean = []
    for mot in ListDB:
        let_mot = {}
        for l in mot:
            let_mot[l] = let_mot[l]+1 if l in let_mot else 1
        toKeep = True
        for (l,_) in rouge:
            if l not in [e[0] for e in orange] and l not in [e[0] for e in vert]:
                if l in mot:
                    toKeep = False                        #print("il y a une rouge qui n'est pas pas verte ni orange, présente ds le mot")
                    break
            elif l in let_mot and let_mot[l] != let_connu[l]:
                toKeep = False                    #print("magie de Jean")
                let_mot[l]-=1
                break
            elif l not in let_mot:
                toKeep = False
                break
        for (l,i) in vert:
            if mot[i] != l:
                toKeep = False                    #print("manque une verte à son indice")
                break
        for (l,i) in orange:
            if mot[i] == l:
                toKeep = False                    #print("une orange n'as pas bougé")
                break
            if l not in mot or let_mot[l]<let_connu[l]:
                toKeep = False                    #print("il manque une orange")
                break
        if toKeep:
            DBclean.append(mot)
    return DBclean

def divisListe(List, n):
    out = []
    newsize = len(List)//n
    for i in range(n):
        out.append(List[i*newsize:(i+1)*newsize])
    rest = List[n*newsize:]
    for i in range(len(rest)):
        out[i].append(rest[i])
    return out

def evalWords(atester, DB):
    out = []
    for firstguess in atester:
        patern_to_proba= {}
        patern_to_matches = {}
        DBsize = len(DB)
        for toGuess in DB:
            patern = evalPatern(toGuess, firstguess)
            patern_to_proba[patern] = 1 if patern not in patern_to_proba else patern_to_proba[patern]+1
            if patern not in patern_to_matches:
                patern_to_matches[patern] = DBsize/len(matchInList(firstguess, patern))


        for pat in patern_to_proba.keys():
            iter = patern_to_proba[pat]
            patern_to_proba[pat] = iter/DBsize


        freqlist = [(freq,pat) for (pat,freq) in patern_to_proba.items()]
        freqlist.sort()

        globalScore = 0
        for freq,pat in freqlist:
            globalScore+=freq*patern_to_matches[pat]
            #print(pat, freq, patern_to_matches[pat])

        #q.put((firstguess, globalScore))
        out.append((globalScore,firstguess))
    return out

def bestSecondchoice():
    firstguess = 'tarie'
    dicopatern = {}
    for toGuess in ListDB:
        patern =  evalPatern(toGuess, firstguess)
        dicopatern[patern] = [toGuess] if patern not in dicopatern else dicopatern[patern]+[toGuess]

    for patern1,liste1 in  dicopatern.items():
        temp = evalWords(liste1, liste1)
        temp.sort()
        scoremax,motmax = temp[-1]
        dicopatern[patern1] = motmax
        print(patern1, motmax)

    print(dicopatern)

def bestFirstchoice():
    for mot in ListDB:
        lemot, lescore = evalWords([mot])
        DBrated.write(lemot+' '+str(lescore)+','+'\n')

    DBrated.close()

def PreshotWordle(toGuess='', usinglast = {'nbDiffMax': 6, 'tailleDBmin': 0}):
    if toGuess == '':
        toGuess = ListDB[randint(0, len(ListDB) - 1)]   #on définit le mot à deviner aléatoirement

    guess1 = 'tarie'
    p1 = evalPatern(toGuess, guess1)
    s1 = set(matchInList(guess1, p1))

    guess2 = dicopatern[p1]
    p2 = evalPatern(toGuess, guess2)
    s2 = set(matchInList(guess2, p2))

    iteration = 2
    ssum = s1 & s2

    guess = guess2

    archiveguess = [guess1, guess2]

    while len(ssum)>1 and iteration < 20:
        iteration += 1

        if len(ssum) > usinglast['tailleDBmin'] and usinglast['nbIdntMin'] <= len(IntersectInDB(ssum)):
            newGuess = BestWithFollowing(ListDB, getLetDiff(ssum))
            guess = newGuess if newGuess != guess else takeaguess(ssum, 'maxScored')
        else:
            guess = takeaguess(ssum, 'maxScored')

        archiveguess.append(guess)
        p = evalPatern(toGuess, guess)
        ssum = ssum & set(matchInList(guess, p))

    return (iteration,archiveguess)

def playAllGamse():
    nbiter = len(ListDB)
    listattempt = []
    winrate = 0
    specialanswer = []
    for i in range(len(ListDB)):
        iteration,answer = PreshotWordle(toGuess=ListDB[i],usinglast={'nbIdntMin':2 , 'tailleDBmin':3})
        if iteration<=6:
            winrate+=1
        else:
            specialanswer.append(answer)

        listattempt.append(iteration)

        pourc = int((i + 1) / nbiter * 100)
        stdout.write('\r[' + '█' * pourc + '░' * (100 - pourc) + f'] tâche {pourc}% complète :')

    print(f'\n{nbiter} essais réalisés')
    print("| coups moyen :",np.mean(listattempt),"| winrate :", winrate / nbiter,"| variance :", np.var(listattempt),"| écart-type :",np.std(listattempt), "|")
    print(specialanswer)



fail = ['verre', 'barbe', 'barre', 'vache', 'gaffe', 'sages', 'verbe', 'hache', 'pipes', 'sures', 'gages', 'pises', 'soums', 'kikis', 'wikis', 'fouge', 'gouge', 'boums', 'barye', 'bures', 'saxes', 'gagee', 'kiwis', 'gazee']


print(PreshotWordle(toGuess='verre',usinglast={'nbIdntMin':3 , 'tailleDBmin':3}))


guess1 = 'tarie'
p1 = evalPatern('verre', guess1)
s1 = set(matchInList(guess1, p1))

guess2 = 'ourse'
p2 = evalPatern('verre', guess2)
s2 = set(matchInList(guess2, p2))

guess3 = 'germe'
p3 = evalPatern('verre', guess3)
s3 = set(matchInList(guess3, p3))


print(len(s1 & s2))
print(len(s1&s2&s3))
print(BestWithFollowing(ListDB, getLetDiff(s1 & s2)))


'''
print(dicopatern['🟥🟥🟥🟥🟥'])

s1 = set(matchInList('tarie', '🟥🟥🟥🟥🟥'))
s2 = set(matchInList('cools', '🟥🟥🟥🟥🟩'))
s3 = set(matchInList('junky', '🟥🟩🟥🟥🟥'))
ssum = s1 & s2 & s3
print(ssum)
print(takeaguess(ssum, 'maxScored'))
print(BestWithFollowing(ListDB, getLetDiff(ssum)))

'''