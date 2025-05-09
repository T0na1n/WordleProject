from multiprocessing import Queue,Process
from Wordle import  *

def PlayXgames(n, q, iter):
    for _ in range(iter):
        q.put(PlayWordle(guesstype=guesstype, printcolorattempt=ColorAttemptInConsole, usinglast=usinglast, optifirstguess=optifirstguess))
def PlayMP():
    processes = []
    results = []
    q = Queue()

    execPerCore = quantAttempt // nbProcess

    for core in range(nbProcess):
        p = Process(target=PlayXgames, args=[core,q,execPerCore])
        processes.append(p)
    for proc in processes:
        proc.start()
    for _ in range(execPerCore):
        for _ in processes:
            results.append(q.get())
    for proc in processes:
        proc.join()
    del processes, q

    for i in range(quantAttempt % nbProcess):
        results.append(PlayWordle(guesstype=guesstype, printcolorattempt=ColorAttemptInConsole, usinglast=usinglast, optifirstguess=optifirstguess))
    return results
