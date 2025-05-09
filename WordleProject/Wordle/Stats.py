
def frqletter(DB):
    "prend en entrée une DB à analyser, renvoi un dico lettre:occurence(indice) stats de la DB"

    dicostat = {'c': [0, 0, 0, 0, 0], 'o': [0, 0, 0, 0, 0], 'm': [0, 0, 0, 0, 0], 'e': [0, 0, 0, 0, 0],
            't': [0, 0, 0, 0, 0], 'a': [0, 0, 0, 0, 0], 'u': [0, 0, 0, 0, 0], 's': [0, 0, 0, 0, 0],
            'i': [0, 0, 0, 0, 0], 'r': [0, 0, 0, 0, 0], 'f': [0, 0, 0, 0, 0], 'n': [0, 0, 0, 0, 0],
            'p': [0, 0, 0, 0, 0], 'q': [0, 0, 0, 0, 0], 'd': [0, 0, 0, 0, 0], 'l': [0, 0, 0, 0, 0],
            'h': [0, 0, 0, 0, 0], 'g': [0, 0, 0, 0, 0], 'v': [0, 0, 0, 0, 0], 'z': [0, 0, 0, 0, 0],
            'j': [0, 0, 0, 0, 0], 'x': [0, 0, 0, 0, 0], 'b': [0, 0, 0, 0, 0], 'y': [0, 0, 0, 0, 0],
            'k': [0, 0, 0, 0, 0], 'w': [0, 0, 0, 0, 0]}
    for mot in DB:
        for i in range(len(mot)):
            dicostat[mot[i]][i] += 1
    l = len(DB)
    for k, v in dicostat.items():
        dicostat[k] = [new / l  for new in v]
    '''dicostatrevers = {v:k for k,v in dicostat.items()}  #lettre:occur -> occur:lettre
    occurence = [e for e in dicostatrevers.keys()]      #extraction et tri de occurences
    occurence.sort(reverse=True)
    letter = [dicostatrevers[e] for e in occurence]     #liste des lettres triées par occurence croissante
    plt.bar(letter, occurence)
    plt.show()'''
    return dicostat                                     #return le dico lettre:occurence

def RateProbaPerFreq(inlist):
    "prend en entrée une liste de mots, renvoie un dico score:mot qui caractérise la probabilité des mots d'être réponse"
    freqletter = frqletter(inlist)          #récup le dico lettre:occurence(ind)
    motToScore = {}
    for mot in inlist:                      #parcours des mots
        score=1
        for i in range(len(mot)):
            score*=freqletter[mot[i]][i]
        if mot in motToScore:
            print(mot)
        motToScore[mot] = score
    return motToScore                                      #return un dico score:mot

def comptage(mot):
    dico={}
    for l in mot :
        if l not in dico:
            dico[l]=1
        else :
            dico[l]+=1
    return dico

def IntersectInDB(DB):
    évalmots = []
    for mot in DB:
        décompmot = []
        for i in range(len(mot)):
            décompmot.append((mot[i], i))
        évalmots.append(set(décompmot))

    intersect = évalmots[0]
    for e in évalmots[1:]:
        intersect = e & intersect
    return list(intersect)

def getLetDiff(DB):

    évalmots = []
    for mot in DB:
        décompmot = []
        for i in range(len(mot)):
            décompmot.append((mot[i], i))
        évalmots.append(set(décompmot))

    intersect = évalmots[0]
    for e in évalmots[1:]:
        intersect = e & intersect


    ldif = set()
    for mot in évalmots:
        for (l, ind) in list(set(mot) - intersect):
            ldif.add(l)
    return list(ldif)

def BestWithFollowing(DB, mustHave):
    scoremax,motmax = 0, DB[0]
    for mot in DB:
        score = 0
        for l in mustHave:
            if l in mot:
                score+=1
        if scoremax<score:
            scoremax, motmax = score, mot
    return motmax

