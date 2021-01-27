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

# Flags for distingushing player turn and win or draw
player = True
status_flag = None


# Action for clicking buttons
def button_click(i, j):
    global player, board

    # Updating maps when it is X's turn
    if not board[i][j]['text'] and player == True:
        board[i][j].config(image=photo_x,width="145",height="153", bg="#67D7A4", activebackground ="#469871")
        player = False
        board[i][j]['text'] = 'X'
        update_label()

    # Updating maps when it is X's turn
    elif not board[i][j]['text'] and player == False:
        board[i][j].config(image=photo_o,width="145",height="153", bg="#82DCE3", activebackground ="#66AEB5")
        player = True
        board[i][j]['text'] = 'O'
        update_label()

    # Clicking filled button
    else:
        tkinter.messagebox.showinfo("Tic-Tac-Toe", "Button already Clicked!")

# Initialize game
def init_game():
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

# Update player turn's label
def update_label():
    # Updating player based on current state
    label_1=tk.Label(text="{}'s turn".format("X" if player else "O"),font=('Ubuntu',18), bg ="#67D7A4" if player else "#82DCE3" ,pady=12, padx=30)
    label_1.grid(row=4,column=2)

def 

init_game()
screen.mainloop()