import numpy as np
import random as r

#faire une grille soluce vide avec 9 listes dedans.
# fonction générer des nombres de 1 à 9 sans doublons
# grillesoluce.append(fonction genere 9 nb)

#fonction random first row(tablde0)

#fonction qui génère des nombres


Tableau = np.zeros((9,9))
print(Tableau)

L = [1,2,3,4,5,6,7,8,9]


def Reset():
    for i in range(1,10):
        L.append(i)
  
def GenEntier():
    return L.pop(r.randint(0,len(L)-1))

def LigneAleatoire(ligne):
    for i in range(9):
        Tableau[ligne][i] = GenEntier()
    Reset()


def CompareLigne(a,b):
    for i in range (0,8):
        if Tableau[a][i] == Tableau[b][i]:
            # print("true")
            return True
    # print("false")
    return False

def CompareColonne(a,b):
    for i in range (0,8):
        if Tableau[i][a] == Tableau[i][b]:
            # print("true")
            return True
    # print("false")
    return False


def ResetLAvecCarre(lin, col):
    list_carre = []
    for i in range(lin,lin+2):
        for j in range(col,col+2):
            list_carre.append(Tableau[i][j])
    while 0 in list_carre:
        list_carre.remove(0)
    # return len(list_carre) != len(set(list_carre))
    
    for value in L:
        while value in list_carre:
            L.remove(value)

def CheckLigne(x,y):
    for i in range(0,8):
        if i == x:
            continue
        else:
            if Tableau[i][y] == Tableau[x][y]:
                return True
    return False

def CheckColonne(x,y):
    for i in range(0,8):
        if i == y:
            continue
        else:
            if Tableau[x][i] == Tableau[x][y]:
                return True
    return False


def InitialisationLignes():

    LigneAleatoire(0)
    LigneAleatoire(3)
    LigneAleatoire(6)

    while CompareLigne(0,3) :
        LigneAleatoire(3) 

    while CompareLigne(0,6) or CompareLigne(3,6):
        LigneAleatoire(6)

def IndiceCarre(i):
    if i >= 6:
        return 6
    elif i <= 3:
        return 0
    else:
        return 3

def Completer():
    for i in range(0, 9):
        if i==0 or i==3 or i==6:
            continue
        else:   
            for j in range(0,9):
                carreX = IndiceCarre(i)
                carreY = IndiceCarre(j)

                while  CheckLigne(i,j) and CheckColonne(i,j):
                    ResetLAvecCarre(carreX,carreY)
                    Tableau[i][j] = GenEntier()
                   


            




InitialisationLignes()
Completer()
print(L)
print(Tableau)


