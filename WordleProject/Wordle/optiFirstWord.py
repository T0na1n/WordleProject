from Wordle import *

atester = ["comme"]
dict = {}
for firstattmpt in atester:
    v=0
    for toGuess in ListDB:
        v+=len(cleanDB(ListDB, firstattmpt, toGuess))
    print(firstattmpt, v/len(ListDB))

