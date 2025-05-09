from mimetypes import guess_extension

from Wordle import *
import matplotlib.pyplot as plt
from sys import stdout
import numpy as np
from multiprocessing import Queue,Process
import time


def PlayXgames(q, iter, guesstype, printcolorattempt, usinglast, optifirstguess):
    for _ in range(iter):
        q.put(PlayWordle(guesstype=guesstype, printcolorattempt=printcolorattempt, usinglast=usinglast, optifirstguess=optifirstguess))
def PlayMP(guesstype,printcolorattempt,usinglast,optifirstguess):

    processes = []
    results = {}
    indcurrentgame = 0
    q = Queue()

    execPerCore = quantAttempt // nbProcess

    for core in range(nbProcess):
        p = Process(target=PlayXgames, args=[q,execPerCore, guesstype,printcolorattempt,usinglast,optifirstguess])
        processes.append(p)
    for proc in processes:
        proc.start()
    for _ in range(execPerCore):
        for _ in processes:
            results[indcurrentgame] = q.get()
            indcurrentgame+=1
            pourc = int((indcurrentgame + 1) / quantAttempt * 100)
            if progressbar:
                stdout.write('\r[' + '█' * pourc + '░' * (100 - pourc) + f'] tâche {pourc}% complète :')
    for proc in processes:
        proc.join()
    del processes, q

    for i in range(quantAttempt % nbProcess):
        results[indcurrentgame+i] = PlayWordle(guesstype=guesstype, printcolorattempt=ColorAttemptInConsole, usinglast=usinglast, optifirstguess=optifirstguess)

    return results
def startGame():
    start = time.time()
    nbtry = {}
    attempt = {}

    if nbProcess>1:
        if ColorAttemptInConsole:
            print("color attempt not available with multiprocessing")
            return
        else:
            attempt = PlayMP(guesstype=guesstype, printcolorattempt=ColorAttemptInConsole, usinglast=usinglast, optifirstguess=optifirstguess)
            for i in range(len(attempt)):
                nbtry[i] = attempt[i][0]
    else:
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
    print('| ',guesstype, " | methode last:", usinglast,"| nb de coups predef :",optifirstguess,"|")
    print("| coups moyen :",np.mean(coups),"| winrate :", win / quantAttempt,"| variance :", np.var(coups),"| écart-type :",np.std(coups), "|")
    print("temps d'execution:", int((time.time()-start)*100)/100, "s")
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


if __name__ == '__main__':

    guesstype = 'random'
    quantAttempt = 5000
    plotting = False
    progressbar = True
    usinglast = True
    optifirstguess = 0
    ColorAttemptInConsole = False
    nbProcess = 4

    optifirstguess = 0
    guesstype = 'random'
    startGame()
    guesstype = 'maxScored'
    startGame()
    guesstype = 'minScored'
    startGame()
    guesstype = 'medScored'
    startGame()



    optifirstguess = 1
    guesstype = 'random'
    startGame()
    guesstype = 'maxScored'
    startGame()
    guesstype = 'minScored'
    startGame()
    guesstype = 'medScored'
    startGame()


    optifirstguess = 2
    guesstype = 'random'
    startGame()
    guesstype = 'maxScored'
    startGame()
    guesstype = 'minScored'
    startGame()
    guesstype = 'medScored'
    startGame()

    if plotting:
        plt.show()



