import numpy as np
import random as r

tab = np.zeros((9,9), dtype=int)


# Initialisation -----------------------------------------------------------------------------------

def GenererCarreAleatoire(x,y):
    liste = [1,2,3,4,5,6,7,8,9]
    r.shuffle(liste)
    for i in range (x, x+3):
        for j in range (y,y+3):
            tab[i][j] = liste.pop()

def Initialisation():
    GenererCarreAleatoire(0,0)
    GenererCarreAleatoire(3,3)
    GenererCarreAleatoire(6,6)

Initialisation()

# conditions sudoku --------------------------------------------------------------------------------

def CheckLigne(tab, lin, col):
    num = tab[lin][col]
    if num == 0:
        return True
    for c in range(len(tab[lin])):
        if c != col and tab[lin][c] == num:
            return False
    return True

def CheckColonne(tab, lin, col):
    num = tab[lin][col]
    if num == 0:
        return True
    for l in range(len(tab[col])):
        if l != lin and tab[l][col] == num:
            return False
    return True

def IndiceCarre(i):
    if i >= 6:
        return 6
    elif i <= 3:
        return 0
    else:
        return 3

def CheckCarre(tab, lin, col):
    carreX = IndiceCarre(lin)
    carreY = IndiceCarre(col)

    listeCarre = []
    for i in range (carreX, carreX+3):
        for j in range (carreY,carreY+3):
            if tab[i][j] != 0:
                listeCarre.append(tab[i][j])
    return len(listeCarre) == len(set(listeCarre))

def CheckTotal(tab,lin,col):
    return CheckLigne(tab, lin, col) and CheckColonne(tab, lin, col) and CheckCarre(tab, lin, col)

# génération de la grille solution --------------------------------------------------------------------------

def RemplirGrille():
    return Backtrack(0, 0)

def Backtrack(lin, col):
    if lin == 9:
        return True

    next_lin, next_col = (lin, col + 1) if col < 8 else (lin + 1, 0)

    if tab[lin][col] != 0:
        return Backtrack(next_lin, next_col)

    for val in range(1, 10):
        tab[lin][col] = val
        if CheckTotal(tab, lin, col):
            if Backtrack(next_lin, next_col):
                return True
        tab[lin][col] = 0

    return False

def Creationtableau():
    Initialisation()

    if RemplirGrille():
        print(tab)
    else:
        print("Échec de la génération.")
  

Creationtableau()


# création grille à trous --------------------------------------------------------------------------

def ViderCases(num):

    indices = [(i, j) for i in range(9) for j in range(9)]
    r.shuffle(indices)
    
    for k in range(num):
        i, j = indices[k]
        tab[i][j] = 0
                    
ViderCases(50)

print(tab)


# algorithme pour vérifier qu'il n'y ait qu'une seule solution -------------------------------------

