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


# création grille à trous avec une seule solution --------------------------------------------------

def CompterSolutions(tab):
    compteur = [0]
    def Solve(lin=0, col=0):
        if lin == 9:
            compteur[0] += 1
            return
        if compteur[0] > 1:  # Stop early if more than one solution
            return
        next_lin, next_col = (lin, col + 1) if col < 8 else (lin + 1, 0)

        if tab[lin][col] != 0:
            Solve(next_lin, next_col)
        else:
            for val in range(1, 10):
                tab[lin][col] = val
                if CheckTotal(tab, lin, col):
                    Solve(next_lin, next_col)
                tab[lin][col] = 0

    Solve()
    return compteur[0]

def ViderCasesUnique(nb_cases_a_enlever, essais_max=500):
    indices = [(i, j) for i in range(9) for j in range(9)]
    nb_supprimees = 0
    essais = 0

    while nb_supprimees < nb_cases_a_enlever and essais < essais_max:
        i, j = r.choice(indices)
        if tab[i][j] == 0:
            essais += 1
            continue

        sauvegarde = tab[i][j]
        tab[i][j] = 0

        copie = np.copy(tab)
        if CompterSolutions(copie) == 1:
            nb_supprimees += 1
        else:
            tab[i][j] = sauvegarde  # restaurer la valeur

        essais += 1

ViderCasesUnique(50)
print(tab)


#check non nécessaire

def est_valide(grille, ligne, col, num):
    # Vérifie la ligne
    if num in grille[ligne]:
        return False

    # Vérifie la colonne
    if num in [grille[i][col] for i in range(9)]:
        return False

    # Vérifie le carré 3x3
    start_ligne, start_col = 3 * (ligne // 3), 3 * (col // 3)
    for i in range(start_ligne, start_ligne + 3):
        for j in range(start_col, start_col + 3):
            if grille[i][j] == num:
                return False

    return True

def trouver_vide(grille):
    for i in range(9):
        for j in range(9):
            if grille[i][j] == 0:
                return i, j
    return None

def compter_solutions(grille):
    pos = trouver_vide(grille)
    if not pos:
        return 1  # Une solution trouvée

    ligne, col = pos
    total = 0
    for num in range(1, 10):
        if est_valide(grille, ligne, col, num):
            grille[ligne][col] = num
            total += compter_solutions(grille)
            grille[ligne][col] = 0  # backtrack

    return total


nb_solutions = compter_solutions(tab)
print("Nombre de solutions :", nb_solutions)






