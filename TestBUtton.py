import tkinter as tk
import random as random
import numpy as np
from customtkinter import *

#region CONSTANTS & VARIABLES
COLORS = {
    "text_primary": "#C56135",
    "text_secondary": "#ED9B40",
    "bg_primary": "#93B1A7",
    "bg_secondary": "#7A918D",
    "bg_tertiary": "#9AC1A2"
}

StrictCheck = True
StrictCheck_init = True

playerTab = np.array([
    [3,9,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,4,6,0],
    [2,0,0,0,0,0,0,0,5],
    [0,7,0,8,0,4,0,1,0],
    [0,3,0,0,2,0,0,0,0],
    [5,0,0,0,6,0,8,0,0],
    [0,1,0,7,3,0,0,2,0],
    [9,0,8,0,5,0,0,0,0],
    [0,0,0,2,0,0,0,0,0]])

answerTab = np.array([
    [3,9,6,4,7,5,2,8,1],
    [1,5,7,3,8,2,4,6,9],
    [2,8,4,9,1,6,7,3,5],
    [6,7,2,8,9,4,5,1,3],
    [8,3,1,5,2,7,6,9,4],
    [5,4,9,1,6,3,8,7,2],
    [4,1,5,7,3,8,9,2,6],
    [9,2,8,6,5,1,3,4,7],
    [7,6,3,2,4,9,1,5,8]])






CurrentBtn = None
CurrentRow = None
CurrentCol = None
CurrentSquare = None
CurrentGrid = playerTab.copy()

# Array_vsplit = np.split(CurrentGrid, 3)
# Array_Squares = [np.split(v, 3, axis= 1) for v in Array_vsplit]
# Array_Squares = [col for row in Array_Squares for col in row]
# Array_Squares = np.array(Array_Squares)





subgrid_frames = [[None] * 3 for _ in range(3)]

ArrayButton = np.empty((9, 9), dtype=object)

err_count = 0
#endregion
#region FONCTIONS
def Compare_Truth(Btn):
    global playerTab
    tup = np.where(ArrayButton == Btn)
    t_x, t_y = tup[0][0], tup[1][0]
    if GetBVal(Btn) == str(answerTab[t_x][t_y]):
        Btn.configure(fg_color = "pale green")
        playerTab[t_x][t_y] = GetBVal(Btn)
    elif GetBVal(Btn) != str(answerTab[t_x][t_y]) and GetBVal(Btn) != 0:
        Btn.configure(fg_color = "red")
        
    

def init_color():
    pass

def StrictCheck_init():
    if StrictCheck_init:
        Array_Truth = playerTab.astype(bool)
        ArrayButton = ArrayButton.configure(Array_Truth)


def SplitSquares(array):
    Array_vsplit = np.split(array, 3)
    Array_Squares = [np.split(v, 3, axis= 1) for v in Array_vsplit]
    Array_Squares = [col for row in Array_Squares for col in row]
    Array_Squares = np.array(Array_Squares)
    return Array_Squares

def onButtonClicked(x,y):
    global CurrentBtn, i_x, i_y,i_sq

    if playerTab[x][y] == 0:
        if StrictCheck:
            if CurrentBtn == ArrayButton[x][y]:
                CurrentBtn.configure(fg_color = 'white')
                CurrentBtn = None
            elif CurrentBtn != ArrayButton[x][y] and CurrentBtn != None:
                CurrentBtn = ArrayButton[x][y]
                CurrentBtn.configure(fg_color = COLORS["bg_secondary"])
                i_x, i_y = x,y
                i_sq = (i_x // 3) * 3 + i_y // 3
            else:
                CurrentBtn = ArrayButton[x][y]
                CurrentBtn.configure(fg_color = COLORS["bg_secondary"])
                i_x, i_y = x,y
                i_sq = (i_x // 3) * 3 + i_y // 3

        elif CurrentBtn == ArrayButton[x][y]:
            for v in R_rep:
                if GetBVal(CurrentBtn) == str(v):
                    CurrentBtn.configure(fg_color = "red")
                    break
                CurrentBtn.configure(fg_color = 'white')
            CurrentBtn = None
        elif CurrentBtn != ArrayButton[x][y] and CurrentBtn != None:
            for v in R_rep:
                if GetBVal(CurrentBtn) == str(v):
                    CurrentBtn.configure(fg_color = "red")
                    break
                CurrentBtn.configure(fg_color = 'white')
            CurrentBtn = ArrayButton[x][y]
            CurrentBtn.configure(fg_color = COLORS["bg_secondary"])
            i_x, i_y = x,y
            i_sq = (i_x // 3) * 3 + i_y // 3
        else:
            CurrentBtn = ArrayButton[x][y]
            CurrentBtn.configure(fg_color = COLORS["bg_secondary"])
            i_x, i_y = x,y
            i_sq = (i_x // 3) * 3 + i_y // 3
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
            Victory = True
            print("Victory!")
            return True

    else:
        CheckRow(CurrentRow)
        #CheckCol(CurrentCol)
        #CheckSquare(CurrentSquare)

def ChangeCellNum(event):
    if CurrentBtn != None and event.char in "123456789":
        if StrictCheck and CurrentGrid[i_x][i_y] == answerTab[i_x][i_y]:
            return
        CurrentBtn.configure(text = event.char,text_color="blue")
        CurrentGrid[i_x][i_y] = event.char
        # if StrictCheck:
        #     if CurrentGrid[i_x][i_y] == answerTab[i_x][i_y]:
        #         playerTab[i_x][i_y] = event.char
        #         CurrentBtn.configure(fg_color = "pale green")
        #     else:
        #         CurrentBtn.configure(fg_color = "red")
        CheckLogic()
        Compare_Truth(CurrentBtn)
        #if GetBVal(CurrentBtn) in R_rep:
            #CurrentBtn.configure(fg_color = "red")
    print(CurrentGrid)

# def CheckLogic():
#     row = CurrentGrid[i_x, :]
#     col = CurrentGrid[:, i_y]
#     if not CheckRow(row) or not CheckCol(col):
#         return False
#       return True

def CheckRow(CurrentRow):
    global R_rep, R_err, err_count
    if StrictCheck:
        RowSol = answerTab[i_x]
        if np.array_equal(CurrentRow,RowSol):
            return True
        
    else:
        if err_count == 0:
            R_err = None
        #creer un array des indices des valeurs != 0
        AU_i = np.argwhere(row)
        print(AU_i)
        AU = np.take(row, AU_i)
        print(AU)
        AU = AU.flatten()

        #Creer un NamedTuple contenant les valeurs et le nombres d'occurences. S'il y a des valeurs répétées, les renvoie
        print(AU)
        val, count = np.unique_counts(AU)
        print(val, count)
        R_rep = val[count > 1]
        print(R_rep)
        print(R_rep.size)
    
        if R_rep.size > 0:
            err_count += 1
            R_err = True
            print(R_err, R_rep.size)
            for button in ArrayButton[i_x]:
                for v in R_rep:
                    if GetBVal(button) == str(v):
                        b_text = button.cget("text")
                        if b_text == str(v):
                            button.configure(fg_color = "red")
        elif R_err == True and R_rep.size == 0:
            print(R_err)
            for button in ArrayButton[i_x]:
                button.configure(fg_color = "white")
            R_err = False
        print(R_err)

            
    # for button in ArrayButton[i_x]:
    #     button.configure(fg_color = "white")
    
        if len(val) == 9 and not R_err:
            return True

        

def GetBVal(Btn):
    B_val = Btn.cget("text")
    return B_val
    
    
#endregion
def launch_sudoku():
    global root, frame, subgrid_frames, ArrayButton, CurrentBtn, CurrentRow, CurrentCol, CurrentSquare, CurrentGrid, Array_Squares

    # (Réinitialise les variables importantes)
    CurrentBtn = None
    CurrentRow = None
    CurrentCol = None
    CurrentSquare = None
    CurrentGrid = playerTab.copy()
    ArrayButton[:] = np.empty((9, 9), dtype=object)
    subgrid_frames[:] = [[None] * 3 for _ in range(3)]

    root = CTk()
    root.bind('<Key>', ChangeCellNum)
    root.title("Sudoku")

    frame = CTkFrame(root, fg_color=COLORS["bg_tertiary"], corner_radius=4, border_width=5, width=800, height=450)
    frame.pack(pady=2, padx=2)

    for i in range(3):
        for j in range(3):
            subgrid = CTkFrame(frame, fg_color=COLORS["bg_tertiary"], corner_radius=0)
            subgrid.grid(row=i, column=j, padx=1, pady=1)
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
    root.mainloop()

