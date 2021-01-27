import tkinter as tk
import tkinter.messagebox

# Creating screen and initial configuration
screen = tk.Tk()
screen.title("Tic Tac Toe")
screen.geometry("450x530")
screen.resizable(0, 0)

# Images for X and O
photo_x = tk.PhotoImage(file="./images/x.png")
photo_o = tk.PhotoImage(file="./images/o.png")

# Initial board game
board = [["" for _ in range(3)] for _ in range(3)]
board_labels = [["" for _ in range(3)] for _ in range(3)]

# Flags for distingushing player turn and win or draw
is_player_X = True
status_flag = None


# Action for clicking buttons
def button_click(i, j):
    global is_player_X, board, board_labels

    # Updating maps when it is X's turn
    if not board_labels[i][j] and is_player_X == True:
        board[i][j].config(image=photo_x,width="145",height="153", bg="#67D7A4", activebackground ="#469871")
        update_map(i, j)


    # Updating maps when it is X's turn
    elif not board_labels[i][j] and is_player_X == False:
        board[i][j].config(image=photo_o,width="145",height="153", bg="#82DCE3", activebackground ="#66AEB5")
        update_map(i, j)
        


def update_map(i,j):
    global is_player_X, board

    # Updating information
    board_labels[i][j] = 'X' if is_player_X else 'O'
    is_player_X = not is_player_X
    update_label()

    # Checking for game over
    is_game_over()

    # Announce final status
    if status_flag != None:
        if status_flag == 0:
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "Draw!")
        elif status_flag == 1:
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "O wins!")
        else:
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "X wins!")
        is_player_X = not is_player_X
        init_game()

def is_game_over():
    global status_flag

    # Checking for draw
    draw_flag = True
    for i in range(3):
        if '' in board_labels[i]:
            draw_flag = False
            break
    status_flag = 0 if draw_flag else None

    # Checking for row winning
    for i in range(3):
        if board_labels[i][0] == board_labels[i][1] == board_labels[i][2] != '':
            if board_labels[i][0] == 'X':
                status_flag = -1
            else:
                status_flag = 1
    
    # Checking for column winning
    for j in range(3):
        if board_labels[0][j] == board_labels[1][j] == board_labels[2][j] != '':
            if board_labels[i][0] == 'X':
                status_flag = -1
            else:
                status_flag = 1
    
    # Checking for top-right to down-left diagonal winning
    if board_labels[0][0] == board_labels[1][1] == board_labels[2][2] != '':
        if board_labels[0][0] == 'X':
            status_flag = -1
        else:
            status_flag = 1

    # Checking for top-left to down-right diagonal winning 
    elif board_labels[0][2] == board_labels[1][1] == board_labels[2][0] != '':
        if board_labels[2][0] == 'X':
            status_flag = -1
        else:
            status_flag = 1

    
# Initialize game
def init_game():
    global board_labels
    for i in range(3):
        for j in range(3):
            # Creating empty buttons
            board[i][j]=tk.Button(text='',width=18,height=9, padx=0, pady = 0,command=lambda r=i,c=j: button_click(r,c))
            board[i][j].grid(row=i,column=j)
            # Creating turn's label
            update_label()
            # Creating reset button
            reset_button=tk.Button(text='Reset',font=('Ubuntu',18), bg='#d4695d', activebackground = '#c46156' ,command=init_game ,pady=12, padx=35)
            reset_button.grid(row=4,column=0)
    # Reseting labels
    board_labels = [["" for _ in range(3)] for _ in range(3)]

# Update is_player_X turn's label
def update_label():
    # Updating is_player_X based on current state
    label_1=tk.Label(text="{}'s turn".format("X" if is_player_X else "O"),font=('Ubuntu',18), bg ="#67D7A4" if is_player_X else "#82DCE3" ,pady=12, padx=30)
    label_1.grid(row=4,column=2)


init_game()
screen.mainloop()