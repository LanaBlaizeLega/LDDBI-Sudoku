import tkinter as tk
import random as random
import numpy as np

MARGE = 20
COTE = 50
LONGUEUR = LARGEUR = MARGE * 2 + COTE * 9

racine = tk.Tk()
racine.title("Sudoku")

grille = tk.Canvas(racine, height = LONGUEUR, width=LARGEUR,)
grille.pack(fill="both", side="top")

matDefaut = np.array([
    [3,9,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,4,6,0],
    [2,0,0,0,0,0,0,0,5],
    [0,7,0,8,0,4,0,1,0],
    [0,3,0,0,2,0,0,0,0],
    [5,0,0,0,6,0,8,0,0],
    [0,1,0,7,3,0,0,2,0],
    [9,0,8,0,5,0,0,0,0],
    [0,0,0,2,0,0,0,0,0]])

def creer_tableau(mat):
    tableau = []
    for ligne in mat:
        tableau.append([])
        for elem in ligne:
            tableau[-1].append(int(elem))
    return tableau
creer_tableau(matDefaut)

def generer_grille(tableau):
    canvas.delete("nombres")
    for r in range(10):
        for c in range(10):
            ans = tableau[r][c]
            if ans != 0:
                x = MARGE + r * COTE + COTE / 2
                y = MARGE + c * COTE + COTE / 2
                orig = tableau[r][c]
                


racine.mainloop()