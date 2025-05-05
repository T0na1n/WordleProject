from Wordle import *
import matplotlib.pyplot as plt
from sys import stdout
import numpy as np
import time
from multiprocessing import Process


def Play(totiter, guesstype, printcolorattempt, usinglast, optifirstguess):
    for i in range(totiter):
        PlayWordle(guesstype=guesstype, printcolorattempt=printcolorattempt,
                   usinglast=usinglast, optifirstguess=optifirstguess)
def startGame():
    nbtry = {}
    attempt = {}

    '''processes = []
    for i in range(nbProcess):
        p = Process(target=Play, args=(quantAttempt/nbProcess, guesstype, ColorAttemptInConsole, usinglast, optifirstguess))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()'''

    for i in range(quantAttempt):
        attempt[i] = PlayWordle(guesstype=guesstype, printcolorattempt=ColorAttemptInConsole, usinglast=usinglast, optifirstguess=optifirstguess)
        nbtry[i] = attempt[i][0]
        pourc = int((i+1) / quantAttempt * 100)

        if progressbar:
            stdout.write('\r[' + '█' * pourc + '░' * (100 - pourc) + f'] tâche {pourc}% complète :')

    print(f'\n{quantAttempt} essais réalisés')

    win = 0
    coups = []
    for iter, coup in nbtry.items():
        coups.append(coup)
        if coup <= 6:
            win += 1
    print(np.mean(coups), win / quantAttempt, np.std(coups), np.var(coups))
    print()

    if plotting:

        couptoratio = {}
        for attempn, coups in nbtry.items():
            couptoratio[coups] = couptoratio[coups] + 1 if coups in couptoratio else 1

        coups = [e for e in couptoratio.keys()]
        coups.sort()
        nbiters = [couptoratio[e] / quantAttempt for e in coups]

        plt.plot(coups, nbiters, label=guesstype)
        plt.legend(loc="upper right")

guesstype = 'random'
quantAttempt = 100
plotting = True
progressbar = True
usinglast = True
optifirstguess = 1
ColorAttemptInConsole = False
nbProcess = 4
startGame()

guesstype = 'maxScored'
startGame()

guesstype = 'medScored'
startGame()

guesstype = 'minScored'
startGame()

guesstype = 'firstoflist'
startGame()



if plotting:
    plt.show()



