from multiprocessing import Pipe,Process
from Wordle import  *
import time
NbCore = 4
GamesPerCore = [10, 1000, 100, 2000]
data = []
def PlayXgames(iter, nbprocess):
    localdata = []
    for i in range(iter):
        localdata.append(["processus n°",nbprocess," itération", i])
    print(localdata)
    return localdata


if __name__ == '__main__':
    processes = []

    for core in range(NbCore):
        p = Process(target=PlayXgames, args=[GamesPerCore[core], core])
        processes.append(p)
        p.start()
    print("finished attribution")

    for process in processes:
        process.join()
    print("finished merging")

    print(data)