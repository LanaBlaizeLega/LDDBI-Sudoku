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

def CheckColonne(a,b):
    for i in range (0,8):
        if Tableau[a][i] == Tableau[b][i]:
            return True
    return False


def InitialisationLignes():

    LigneAleatoire(0)
    LigneAleatoire(3)
    LigneAleatoire(6)

    while CheckColonne(0,3) :
        LigneAleatoire(3) 

    while CheckColonne(0,6) and CheckColonne(3,6):
        LigneAleatoire(6)

InitialisationLignes()
print(L)
print(Tableau)



