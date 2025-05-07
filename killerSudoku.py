from customtkinter import *
import random
import numpy as np
import tkinter as tk

# Définition des cages (somme + cellules de chaque cage)
killer_cages = [
    {"sum": 10, "cells": [(0, 0), (1, 0)]},
    {"sum": 15, "cells": [(0, 1), (0, 2), (1, 2)]},
    {"sum": 20, "cells": [(1, 1), (2, 1), (2, 2)]},
    {"sum": 8, "cells": [(3, 3), (3, 4)]},
    {"sum": 12, "cells": [(4, 4), (5, 4)]},
]

SETCOLORS = {
    "text_primary": "#C56135",
    "text_secondary": "#ED9B40",
    "bg_primary": "#93B1A7",
    "bg_secondary": "#7A918D",
    "bg_tertiary": "#9AC1A2"
}
# La grille Sudoku d'origine
grid = np.array([
    [3, 9, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 4, 6, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 5],
    [0, 7, 0, 8, 0, 4, 0, 1, 0],
    [0, 3, 0, 0, 2, 0, 0, 0, 0],
    [5, 0, 0, 0, 6, 0, 8, 0, 0],
    [0, 1, 0, 7, 3, 0, 0, 2, 0],
    [9, 0, 8, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0]
])

# Palette de couleurs aléatoires pour les cages
colors = ["#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC", "#FFCCFF", "#CCFFFF", "#FFD700", "#FFA07A", "#98FB98"]
random.shuffle(colors)

# Associer une couleur à chaque cage
for i, cage in enumerate(killer_cages):
    cage["color"] = colors[i % len(colors)]

# Fonction pour obtenir les informations sur la cage
def get_cage_info(x, y):
    for cage in killer_cages:
        if (x, y) in cage["cells"]:
            is_first_cell = (x, y) == cage["cells"][0]
            return cage["sum"] if is_first_cell else None, cage["color"]
    return None, "white"

# Création de la fenêtre principale
root = CTk()
root.title("Killer Sudoku")

# Frame principal pour contenir tout
frame = CTkFrame(root, fg_color=SETCOLORS["bg_tertiary"], corner_radius=10)
frame.pack(pady=2, padx=2)

# Créer une structure de sous-grilles 3x3
subgrid_frames = np.empty((3, 3), dtype=object)

for i in range(3):
    for j in range(3):
        subgrid = CTkFrame(frame, fg_color=SETCOLORS["bg_tertiary"], corner_radius=0)
        subgrid.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")  # Espacer les sous-grilles
        subgrid_frames[i, j] = subgrid

# Créer les boutons pour chaque case de la grille
for i in range(9):
    for j in range(9):
        # Trouver la cage et la couleur correspondante
        sum_text, bg_color = get_cage_info(i, j)
        sudoku_value = str(grid[i][j]) if grid[i][j] != 0 else ""

        # Choisir le sous-frame en fonction de la position (i, j) pour chaque bloc 3x3
        subgrid_frame = subgrid_frames[i // 3, j // 3]

        # Créer un bouton pour chaque case
        cell_frame = CTkFrame(subgrid_frame, fg_color=bg_color, width=50, height=50, corner_radius=0, border_width=1, border_color="black")
        cell_frame.grid(row=i % 3, column=j % 3, padx=1, pady=1)

        btn = CTkButton(
            cell_frame,
            text=sudoku_value,
            width=50, height=50,
            font=("Arial", 16, "bold"),
            fg_color="transparent",
            text_color="black",
            hover_color=SETCOLORS["bg_secondary"],
            corner_radius=0
        )
        btn.pack()

        # Si une somme existe pour cette cellule (c'est le premier élément de la cage), afficher la somme
        if sum_text is not None:
            sum_label = CTkLabel(cell_frame, text=str(sum_text), font=("Arial", 10), text_color="black", fg_color="transparent", width=1, height=1)
            sum_label.place(relx=0.05, rely=0.05, anchor="nw")  # En haut à gauche

root.mainloop()
