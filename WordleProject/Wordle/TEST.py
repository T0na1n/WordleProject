from multiprocessing import Pipe,Process
from Wordle import  *
NbCore = 4
NbIter = 100

def PlayXgames(iter, q):
    for _ in range(iter):
        q.send(PlayWordle())

if __name__ == '__main__':
    pipesOut,processes = [],[]

    for _ in range(NbCore):
        dataout,datain = Pipe()
        p = Process(target=PlayXgames, args=(NbIter//NbCore, datain))
        p.start()
        pipesOut.append(dataout)
        processes.append(p)

    dataout, datain = Pipe()
    p = Process(target=PlayXgames, args=(NbIter%NbCore, datain))
    p.start()
    pipesOut.append(dataout)
    processes.append(p)
    print("finished attribution")
    print(len(pipesOut))

    data = 0
    while data<NbIter:
        for pipe in pipesOut:
            print(pipe.recv())
            data+=1

    for process in processes:
        process.join()
        print("joined 1 process")
    print("finished merging")

