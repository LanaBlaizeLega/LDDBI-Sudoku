import tkinter as tk
from tkinter import StringVar
from customtkinter import *
import numpy as np
import random as r
import os

# === Constants ===
COLORS = {
    "text_primary": "#C56135",
    "text_secondary": "#ED9B40", 
    "bg_primary": "#93B1A7",
    "bg_secondary": "#7A918D",
    "bg_tertiary": "#9AC1A2"
}
FONTS = {
    "main": "Segoe UI",
    "secondary": "Arial"
}
CREDITS = ["Abigael Roche", "Lana Blaise", "Félix Plaine-Forgues"]
DIFFICULTY_LABELS = ["Impossible", "Master", "Normal", "Easy"]
DIFFICULTY_DESCRIPTIONS = [
    "mathematically impossible",
    "so... you Do want to be alone",
    "Still want to have fun eh",
    "Dont need much time to do this one"
]

# === Globals ===
grid_labels = []
precomputed_empty_cells = []
visible_mask = np.full((9, 9), False)  # Initial mask where False = empty (dark), True = filled (light)
generationTab = np.zeros((9,9), dtype=int)
playerTab = np.zeros((9,9), dtype=int)
answerTab = np.zeros((9,9), dtype=int)
baseTab = np.zeros((9,9), dtype=int)
DifficultySliderValue = 40

StrictCheck = True
StrictCheck_init = True

CurrentBtn = None
CurrentRow = None
CurrentCol = None
CurrentSquare = None
CurrentGrid = playerTab.copy()
subgrid_frames = [[None] * 3 for _ in range(3)]
ArrayButton = np.empty((9, 9), dtype=object)
err_count = 0
lives = 3

seconds = 0
running = False
timer_id = None  

# === SudokuGenerationFunc

def GenererCarreAleatoire(x,y):
    liste = [1,2,3,4,5,6,7,8,9]
    r.shuffle(liste)
    for i in range (x, x+3):
        for j in range (y,y+3):
            generationTab[i][j] = liste.pop()

def Initialisation():
    GenererCarreAleatoire(0,0)
    GenererCarreAleatoire(3,3)
    GenererCarreAleatoire(6,6)

def CheckLigne(generationTab, lin, col):
    num = generationTab[lin][col]
    if num == 0:
        return True
    for c in range(len(generationTab[lin])):
        if c != col and generationTab[lin][c] == num:
            return False
    return True

def CheckColonne(generationTab, lin, col):
    num = generationTab[lin][col]
    if num == 0:
        return True
    for l in range(len(generationTab[col])):
        if l != lin and generationTab[l][col] == num:
            return False
    return True

def IndiceCarre(i):
    if i >= 6:
        return 6
    elif i <= 3:
        return 0
    else:
        return 3

def CheckCarre(generationTab, lin, col):
    carreX = IndiceCarre(lin)
    carreY = IndiceCarre(col)

    listeCarre = []
    for i in range (carreX, carreX+3):
        for j in range (carreY,carreY+3):
            if generationTab[i][j] != 0:
                listeCarre.append(generationTab[i][j])
    return len(listeCarre) == len(set(listeCarre))

def CheckTotal(generationTab,lin,col):
    return CheckLigne(generationTab, lin, col) and CheckColonne(generationTab, lin, col) and CheckCarre(generationTab, lin, col)

def RemplirGrille():
    return Backtrack(0, 0)

def Backtrack(lin, col):
    liste = [1,2,3,4,5,6,7,8,9]

    if lin == 9:
        return True

    next_lin, next_col = (lin, col + 1) if col < 8 else (lin + 1, 0)

    if generationTab[lin][col] != 0:
        return Backtrack(next_lin, next_col)

    for val in liste:
        generationTab[lin][col] = val
        if CheckTotal(generationTab, lin, col):
            if Backtrack(next_lin, next_col):
                return True
        generationTab[lin][col] = 0

    return False

def Creationtableau():
    global answerTab
    Initialisation()

    if RemplirGrille():
        print(generationTab)
        answerTab = generationTab.copy()
    else:
        print("Échec de la génération.")
  
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

def ViderCases(nb_cases_a_enlever, essais_max=500):
    indices = [(i, j) for i in range(9) for j in range(9)]
    nb_supprimees = 0
    essais = 0
    tab = answerTab.copy()
    global playerTab, baseTab
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
    playerTab = tab.copy()
    baseTab = tab.copy()

# === InGameFunc ===

def Compare_Truth(Btn):
    global playerTab, CurrentBtn, err_count, lives
    # renvoie un tuple contenant les 2 indices de bouton
    tup = np.where(ArrayButton == Btn)
    t_x, t_y = tup[0][0], tup[1][0]
    # reponse correcte
    if GetBVal(Btn) == str(answerTab[t_x][t_y]):
        Btn.configure(fg_color = "pale green")
        playerTab[t_x][t_y] = GetBVal(Btn)
        CurrentBtn = None
    # reponse incorrecte
    elif GetBVal(Btn) != str(answerTab[t_x][t_y]) and GetBVal(Btn) != 0:
        Btn.configure(fg_color = "red")
        err_count += 1
        lives -= 1
        gameMenuLives.configure(text= "vie(s) restante(s) : " + str(lives) + "/3")
        print(err_count)
        CurrentBtn = None
        if lives == 0:
            loss()
            


def loss():
    global running,lives
    for subgrid in gameGridFrame.winfo_children():
        for btn in subgrid.winfo_children():
            btn.configure(state= 'disabled')
    lives = 3
    stop_timer()
    show_menu(LossMenu)
    
def win():
    global running, lives
    running = False
    show_menu(WinMenu)
    update_win_timer()
    stop_timer()
    lives = 3
    for subgrid in gameGridFrame.winfo_children():
        for btn in subgrid.winfo_children():
            btn.configure(state= 'disabled')
def SplitSquares(array):
    # renvoie un carré des carrés 3x3
    Array_vsplit = np.split(array, 3)
    Array_Squares = [np.split(v, 3, axis= 1) for v in Array_vsplit]
    Array_Squares = [col for row in Array_Squares for col in row]
    Array_Squares = np.array(Array_Squares)
    return Array_Squares

def onButtonClicked(x,y):
    # change la coloration du case choisi 
    global CurrentBtn, i_x, i_y,i_sq

    if playerTab[x][y] == 0:
        if StrictCheck:
            if CurrentBtn == ArrayButton[x][y]:
                CurrentBtn.configure(fg_color = 'white')
                CurrentBtn = None
            elif CurrentBtn != ArrayButton[x][y] and CurrentBtn != None:
                if GetBVal(CurrentBtn) == '' or GetBVal(CurrentBtn) == None:
                    CurrentBtn.configure(fg_color = 'white')
                elif GetBVal(CurrentBtn) != str(answerTab[x][y]):
                    CurrentBtn.configure(fg_color = "red")
                CurrentBtn = ArrayButton[x][y]
                CurrentBtn.configure(fg_color = COLORS["bg_secondary"])
                i_x, i_y = x,y
                i_sq = (i_x // 3) * 3 + i_y // 3
            else:
                CurrentBtn = ArrayButton[x][y]
                CurrentBtn.configure(fg_color = COLORS["bg_secondary"])
                i_x, i_y = x,y
                i_sq = (i_x // 3) * 3 + i_y // 3

        #elif CurrentBtn == ArrayButton[x][y]:
            #for v in R_rep:
                #if GetBVal(CurrentBtn) == str(v):
                    #CurrentBtn.configure(fg_color = "red")
                    #break
                #CurrentBtn.configure(fg_color = 'white')
            #CurrentBtn = None
        #elif CurrentBtn != ArrayButton[x][y] and CurrentBtn != None:
            #for v in R_rep:
                #if GetBVal(CurrentBtn) == str(v):
                    #CurrentBtn.configure(fg_color = "red")
                    #break
                #CurrentBtn.configure(fg_color = 'white')
            #CurrentBtn = ArrayButton[x][y]
            #CurrentBtn.configure(fg_color = COLORS["bg_secondary"])
            #i_x, i_y = x,y
            #i_sq = (i_x // 3) * 3 + i_y // 3
        #else:
            #CurrentBtn = ArrayButton[x][y]
            #CurrentBtn.configure(fg_color = COLORS["bg_secondary"])
            #i_x, i_y = x,y
            #i_sq = (i_x // 3) * 3 + i_y // 3
    if CurrentBtn:
        GetBtnPos(i_x,i_y,i_sq)
        CheckLogic()

def GetBtnPos(i_x, i_y, i_sq):
    global CurrentRow, CurrentCol, CurrentSquare
    CurrentRow = CurrentGrid[i_x, :]
    CurrentCol = CurrentGrid[:, i_y]
    CurrentSquare = Array_Squares[i_sq]
    return CurrentRow, CurrentCol, CurrentSquare

def CheckLogic():
    if StrictCheck:
        if np.array_equal(CurrentGrid,answerTab):
            win()
            return True
    else:
        CheckRow(CurrentRow)

def ChangeCellNum(event):
    # change le chiffre dans le case ou l'efface
    if CurrentBtn != None and event.char in "123456789":
        if StrictCheck and CurrentGrid[i_x][i_y] == answerTab[i_x][i_y]:
            return
        CurrentBtn.configure(text = event.char,text_color="blue")
        CurrentGrid[i_x][i_y] = event.char
        CheckLogic()
        Compare_Truth(CurrentBtn)
    elif event.char == "0" and CurrentBtn != None:
        CurrentGrid[i_x][i_y] = event.char
        CurrentBtn.configure(text = None, fg_color = "white")
    print(CurrentGrid)

def CheckRow(CurrentRow):
    global R_rep, R_err, err_count
    if StrictCheck:
        RowSol = answerTab[i_x]
        if np.array_equal(CurrentRow,RowSol):
            return True  
    #else:
        #if err_count == 0:
            #R_err = None
        #creer un array des indices des valeurs != 0
        #AU_i = np.argwhere(row)
        #print(AU_i)
        #AU = np.take(row, AU_i)
        #print(AU)
        #AU = AU.flatten()

        #Creer un NamedTuple contenant les valeurs et le nombres d'occurences. S'il y a des valeurs répétées, les renvoie
        #print(AU)
        #val, count = np.unique_counts(AU)
        #print(val, count)
        #R_rep = val[count > 1]
        #print(R_rep)
        #print(R_rep.size)
    
        #if R_rep.size > 0:
            #err_count += 1
            #R_err = True
            #print(R_err, R_rep.size)
            #for button in ArrayButton[i_x]:
                #for v in R_rep:
                    #if GetBVal(button) == str(v):
                        #b_text = button.cget("text")
                        #if b_text == str(v):
                           # button.configure(fg_color = "red")
        #elif R_err == True and R_rep.size == 0:
            #print(R_err)
            #for button in ArrayButton[i_x]:
                #button.configure(fg_color = "white")
            #R_err = False
        #print(R_err)

        #if len(val) == 9 and not R_err:
            #return True

def GetBVal(Btn):
    B_val = Btn.cget("text")
    return B_val

def reveal_cell():
    # attribue la valeur correcte à l'un des cases vides
    global CurrentGrid, playerTab, ArrayButton, EmptyCells, CurrentRow
    EmptyCells = np.argwhere(CurrentGrid == 0)
    r_cell = np.random.randint(low=0, high=EmptyCells.shape[0])
    r_x, r_y = EmptyCells[r_cell][0], EmptyCells[r_cell][1]
    CurrentGrid[r_x][r_y] = answerTab[r_x][r_y]
    playerTab[r_x][r_y] = answerTab[r_x][r_y]
    ArrayButton[r_x][r_y].configure(text=str(answerTab[r_x][r_y]), fg_color = "pale green")
    CurrentRow = CurrentGrid[r_x, :]
    CheckLogic()

      
#endregion

def launch_sudoku():
    global gameGridFrame, subgrid_frames, ArrayButton, CurrentBtn, CurrentRow, CurrentCol, CurrentSquare, CurrentGrid, Array_Squares, parent_frame

    # (Réinitialise les variables importantes)
    gameMenuLives.configure(text= "vie(s) restante(s) : " + str(lives) + "/3")
    CurrentBtn = None
    CurrentRow = None
    CurrentCol = None
    CurrentSquare = None
    CurrentGrid = playerTab.copy()
    ArrayButton[:] = np.empty((9, 9), dtype=object)
    subgrid_frames[:] = [[None] * 3 for _ in range(3)]
    gameGridFrame = CTkFrame(GameMenu, fg_color=COLORS["bg_tertiary"], corner_radius=4, border_width=5,width = 1280, height = 720)
    gameGridFrame.pack(pady=2, padx=2)

    for i in range(3):
        for j in range(3):
            subgrid = CTkFrame(gameGridFrame, fg_color=COLORS["bg_tertiary"], corner_radius=0)
            subgrid.grid(row=i, column=j, padx=2, pady=2)
            subgrid_frames[i][j] = subgrid

    for i in range(9):
        for j in range(9):
            parent_frame = subgrid_frames[i // 3][j // 3]

            e = CTkButton(
                parent_frame,
                text=str(playerTab[i][j]) if playerTab[i][j] != 0 else "",
                width=50, height=50,
                font=("Arial", 16),
                fg_color="white" if playerTab[i][j] == 0 else "pale green",
                text_color="black",
                hover_color=COLORS["bg_secondary"],
                border_color=COLORS["bg_primary"],
                border_width=2,
                command=lambda x=i, y=j: onButtonClicked(x, y)
            )

            e.grid(row=i % 3, column=j % 3)
            ArrayButton[i][j] = e

    Array_Squares = SplitSquares(CurrentGrid)
# === timer fonc ===
def update_timer():
    global seconds, timer_id
    seconds += 1
    minutes = seconds // 60
    secs = seconds % 60
    timer_label.configure(text=f"Temps: {minutes:02}:{secs:02}")
    timer_id = app.after(1000, update_timer)

def update_win_timer():
    global seconds, timer_id
    seconds += 1
    minutes = seconds // 60
    secs = seconds % 60
    win_timer_label.configure(text=f"Temps: {minutes:02}:{secs:02}")
    
def start_timer():
    global running, timer_id
    if running:
        stop_timer()  
    running = True
    update_timer()

def stop_timer():
    global running, timer_id
    running = False
    if timer_id is not None:
        app.after_cancel(timer_id)
        timer_id = None

def reset_timer():
    global seconds
    stop_timer()
    seconds = 0
    timer_label.configure(text="Temps: 00:00")

# === Tkinter setup ===

app = CTk()
app.bind('<Key>', ChangeCellNum)
width, height = app.winfo_screenwidth(), app.winfo_screenheight()
app.geometry(f"{width}x{height}")
app.title("Kudoku Sudoku")
try:
    app.state('zoomed')
except tk.TclError:
    app.wm_attributes("-zoomed", True)

def precompute_empty_cells():
    
    indices = [(i, j) for i in range(9) for j in range(9)]
    
    r.shuffle(indices)
    return indices

# genère un ordre de case vide 

precomputed_empty_cells = precompute_empty_cells()

def update_difficulty(val):
    global DifficultySliderValue
    DifficultySliderValue = val
    num_empty_cells = int(val)
    apply_mask_to_grid(num_empty_cells)
    thresholds = [65, 49, 33, 17]
    for i, threshold in enumerate(thresholds):
        if val >= threshold:
            selected_difficulty = i
            break
    DifficultyPanel.configure(
        text=f"{DIFFICULTY_LABELS[selected_difficulty]} - {DIFFICULTY_DESCRIPTIONS[selected_difficulty]}"
    )
    NumberOfDigitPanel.configure(text=f" number of digits : {int(81 - val)}")

def apply_mask_to_grid(n_masques):
    global visible_mask
    visible_mask = np.full((9, 9), True)  # Start by assuming all cells are filled (light)
    
    # Mark the first n_masques cells as empty (dark)
    for idx in range(n_masques):
        i, j = precomputed_empty_cells[idx]
        visible_mask[i][j] = False  # Set as empty (dark)
    
    update_grid_display()

def update_grid_display():
    # Update only the cells that need to change (i.e., become dark or light)
    for i in range(9):
        for j in range(9):
            grid_labels[i][j].configure(
                fg_color=COLORS["text_secondary"] if visible_mask[i][j] else COLORS["text_primary"]
            )

def GameMenuBackButton():
    show_menu(MainMenu)
    global generationTab, playerTab, answerTab, baseTab
    for widget in gameGridFrame.winfo_children():
        widget.destroy()
    gameGridFrame.destroy()
    generationTab = np.zeros((9,9), dtype=int)
    playerTab = np.zeros((9,9), dtype=int)
    answerTab = np.zeros((9,9), dtype=int)
    baseTab = np.zeros((9,9), dtype=int)

def generate_game():
    global lives,err_count,generationTab,playerTab,answerTab,baseTab
    generationTab = np.zeros((9,9), dtype=int)
    playerTab = np.zeros((9,9), dtype=int)
    answerTab = np.zeros((9,9), dtype=int)
    baseTab = np.zeros((9,9), dtype=int)

    Initialisation()
    Creationtableau()
    ViderCases(int(DifficultySliderValue))
    lives = 3
    err_count = 0
    show_menu(GameMenu)
    launch_sudoku()
    reset_timer()
    start_timer()

    print("Game generated!")

def switch_theme():
    mode = light_switch_var.get()
    set_appearance_mode(mode)
    print(f"Switched to {mode} mode.")

def show_menu(menu):
    for m in Menus:
        m.pack_forget()
    menu.pack(fill="both", expand=True, padx=20, pady=20)

def pause():
    show_menu(PauseMenu)
    stop_timer()

def unpause():
    show_menu(GameMenu)
    start_timer()

def load_progress(file):
    data = np.load(file)
    return data['timer'].item(), data['joueur'], data['base'], data['solution'], data['vies']

def LoadSudoku(file):
    global seconds,playerTab,baseTab,answerTab,lives
    seconds,playerTab,baseTab,answerTab,lives = load_progress(file)

    show_menu(GameMenu)
    launch_sudoku()
    start_timer()

def demander_nom_fichier():
    filename = filedialog.asksaveasfilename(
        defaultextension=".npz",
        filetypes=[("Fichiers NumPy", "*.npz")],
        title="Enregistrer la progression"
    )
    if filename:
        save_progress(filename,seconds,playerTab,baseTab,answerTab,lives)
        update_combobox_values()

def save_progress(file, t, joueur, base, solution,vies):
    np.savez(file, timer=t, joueur=joueur, base=base, solution=solution,vies = vies)

def update_combobox_values():
    saves = [f for f in os.listdir(script_dir) if f.endswith('.npz')]
    ListeDeSaves.configure(values=saves)
    if saves:
        ListeDeSaves.set(saves[-1])

def generate_prefab_sudoku(name="prefab_sudoku.npz", holes=40):
    global playerTab,baseTab,answerTab,generationTab

    generationTab = np.zeros((9,9), dtype=int)
    playerTab = np.zeros((9,9), dtype=int)
    answerTab = np.zeros((9,9), dtype=int)
    baseTab = np.zeros((9,9), dtype=int)

    Initialisation()
    Creationtableau()
    ViderCases(holes)
    
    filename = os.path.join(script_dir, name)
    save_progress(filename, 0, playerTab, baseTab, answerTab,3)
    update_combobox_values()  

def PrefabMaking():
    thresholds = [65, 49, 33, 17]
    
    for i in range(20, 55, 5):
        for n, threshold in enumerate(thresholds):
            if i >= threshold:
                difficulty = n
                break
        else:
            # Si aucun seuil n'est respecté (donc i > tous les seuils)
            difficulty = len(thresholds)

        generate_prefab_sudoku(f"{DIFFICULTY_LABELS[difficulty]} {i} trous", i)

def Quit():
    app.destroy()
# === GUI Menus ===
MainMenu = CTkFrame(app)
SecondMenu = CTkFrame(app)
GameMenu = CTkFrame(app)
LoadMenu = CTkFrame(app)
PauseMenu = CTkFrame(app)
LossMenu = CTkFrame(app)
WinMenu = CTkFrame(app)
Menus = [MainMenu, SecondMenu,GameMenu,LoadMenu,PauseMenu,LossMenu,WinMenu]

# MainMenu Widgets
#PrefabBTN = CTkButton(MainMenu,text="prefab",command=PrefabMaking)
MainTitle = CTkLabel(MainMenu, text="Kudoku Sudoku", font=(FONTS["main"], height // 5), text_color=COLORS["text_secondary"])
PlayButton = CTkButton(MainMenu, text="Play", command=lambda: show_menu(SecondMenu), corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))
QuitButton = CTkButton(MainMenu, text="quit", command=Quit, corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))
ReloadButton = CTkButton(MainMenu, text="Reload", command=lambda : show_menu(LoadMenu), corner_radius=32,
                         hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                         font=(FONTS["secondary"], height // 15))
light_switch_var = StringVar(value="dark")
LightSwitch = CTkSwitch(MainMenu, text="LightMode", variable=light_switch_var, onvalue="dark", offvalue="light",
                        command=switch_theme, progress_color=COLORS["text_primary"])
Credits = CTkLabel(MainMenu, text="Created by:\n" + "\n".join(f"{' ' * (i*12)}{name}" for i, name in enumerate(CREDITS)),
                   font=(FONTS["secondary"], height // 40), text_color=COLORS["text_secondary"])

Credits.place(rely=0.95, relx=0, x=0, y=0, anchor=tk.SW)
MainTitle.pack(side="top", fill=tk.X)
PlayButton.pack(pady=10)

ReloadButton.pack(pady=10)
LightSwitch.pack(side="bottom")
QuitButton.pack(pady=10,anchor=SE,side=BOTTOM)

#PrefabBTN.pack()
# SecondMenu Widgets
GenerateButton = CTkButton(SecondMenu, text="Generate", command=generate_game, corner_radius=32,
                           hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                           font=(FONTS["secondary"], height // 15))
BackButton = CTkButton(SecondMenu, text="Back", command=lambda: show_menu(MainMenu), corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))
DifficultyPanel = CTkLabel(SecondMenu, text="", font=(FONTS["main"], height // 40), text_color=COLORS["text_secondary"])
NumberOfDigitPanel = CTkLabel(SecondMenu, text="", font=(FONTS["secondary"], height // 45))
DifficultySlider = CTkSlider(SecondMenu, from_=0, to=81, command=update_difficulty, number_of_steps=81,
                             orientation='vertical', progress_color=COLORS["text_secondary"])

grid_frame = CTkFrame(SecondMenu)
for i in range(9):
    row = []
    for j in range(9):
        label = CTkLabel(grid_frame, text="", width=40, height=40, font=(FONTS["secondary"], 20),
                         corner_radius=8, fg_color=COLORS["bg_primary"])
        label.grid(row=i, column=j, padx=2, pady=2)
        row.append(label)
    grid_labels.append(row)

# Layout
BackButton.grid(row=7, column=2, columnspan=2)
GenerateButton.grid(row=5, column=2, columnspan=2)
DifficultySlider.grid(row=2, column=5, rowspan=5)
DifficultyPanel.grid(row=1, column=6, columnspan=5)
NumberOfDigitPanel.grid(row=4, column=3)
grid_frame.grid(row=3, column=6, rowspan=5, columnspan=5)

# GameMenu Widgets
BtnFrame = CTkFrame(GameMenu)
gameGridFrame = CTkFrame(GameMenu)
gameMenuLives = CTkLabel(GameMenu,text= "vie(s) restante(s) : " + str(lives) + "/3")
gameMenuBackButton = CTkButton(BtnFrame, text="Back", command=GameMenuBackButton, corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))
saveButton = CTkButton(BtnFrame, text="save", command=demander_nom_fichier, corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))

pauseButton = CTkButton(BtnFrame, text="pause", command=pause, corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))

timer_label = CTkLabel(GameMenu, text="Temps: 00:00",font=(FONTS["secondary"], height // 20))
hintButton = CTkButton(GameMenu, text="Aide", fg_color=COLORS["text_secondary"], font=(FONTS["secondary"], height // 20), command=reveal_cell)


hintButton.pack(anchor=E)
timer_label.pack(pady = 10)
gameMenuLives.pack(pady = 10)
BtnFrame.pack(side=BOTTOM,pady = 10)
saveButton.pack(side=LEFT,padx = 10)
pauseButton.pack(side=LEFT,padx = 10)
gameMenuBackButton.pack(side=RIGHT,padx = 10)
# === PauseMenu ===

UnpauseButton = CTkButton(PauseMenu, text="UN - Pause", command=unpause, corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))

UnpauseButton.pack(side=LEFT,expand=True)
# === LossMenu ===
LossLabel = CTkLabel(LossMenu, text="Perdu !", font=(FONTS["main"], height // 5), text_color=COLORS["text_secondary"])


BackButton = CTkButton(LossMenu, text="Back", command=GameMenuBackButton, corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))
LossLabel.pack(expand=True)
BackButton.pack(expand=True)
# === WinMenu ===
WinLabel = CTkLabel(WinMenu, text="Gagné!", font=(FONTS["main"], height // 5), text_color=COLORS["text_secondary"])


WinBackButton = CTkButton(WinMenu, text="Back", command=GameMenuBackButton, corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))

win_timer_label = CTkLabel(WinMenu, text="Temps: 00:00",font=(FONTS["secondary"], height // 20))
win_timer_label.pack()
WinLabel.pack(expand=True)
WinBackButton.pack(expand=True)

# === LoadMenu ===
script_dir = os.path.dirname(os.path.abspath(__file__))
saves = [f for f in os.listdir(script_dir) if f.endswith('.npz')]

ListeDeSaves = CTkComboBox(LoadMenu,values=saves,command=LoadSudoku)
BackButtonBis = CTkButton(LoadMenu, text="Back", command=lambda: show_menu(MainMenu), corner_radius=32,
                       hover_color=COLORS["text_primary"], fg_color=COLORS["text_secondary"],
                       font=(FONTS["secondary"], height // 15))

ListeDeSaves.pack(side = LEFT,expand=True)
BackButtonBis.pack(side = LEFT,expand=True)



# Initial state
update_difficulty(40)
show_menu(MainMenu)

# Start Tkinter main loop
app.mainloop()
print(generationTab)
