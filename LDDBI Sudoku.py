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
    global orig
    tableau = []
    for ligne in mat:
        tableau.append([])
        for elem in ligne:
            tableau[-1].append(int(elem))
    orig = tableau
    return tableau

def generer_grille(tableau):
    global ans_grille
    ans_grille = np.zeros((9,9))
    grille.delete("nombres")
    for r in range(9):
        for c in range(9):
            ans = tableau[r][c]
            if ans != 0:
                x = MARGE + r * COTE + COTE / 2
                y = MARGE + c * COTE + COTE / 2
                orig = tableau[r][c]
                couleur = "gray" if ans == orig else "green"
                grille.create_text(x, y, text = ans, tags = "nombres", fill = couleur)
                ans_grille[r][c] = ans

                grille.bind("<Button-1>", on_clique_cel)
                grille.bind("<Key>", on_cle_appui)
    print(ans_grille)

def on_clique_cel(event):
    global focus_c, focus_r
    x, y = event.x, event.y
    focus_r, focus_c = (y - MARGE) / COTE, (x - MARGE) / COTE



def on_cle_appui(event):
  if event.char in "1234567890" and (focus_r, focus_c) != (orig[focus_r], orig[focus_r]):
       ans_grille[focus_r][focus_c] = int(event.char)
       print(ans_grille)



generer_grille(creer_tableau(matDefaut))
racine.mainloop()