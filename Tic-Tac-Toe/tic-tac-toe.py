import tkinter as tk
import copy
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

    # AI action if it is legal
    if not is_player_X:
        currnet = Node(board_labels, True)
        action = alpha_beta_search(currnet, i ,j)
        board[action[0]][action[1]].after(500, lambda: board[action[0]][action[1]].invoke())
        


def update_map(i,j):
    global is_player_X, board

    # Updating information
    board_labels[i][j] = 'X' if is_player_X else 'O'
    is_player_X = not is_player_X
    update_label()

    # Checking for game over
    is_game_over(board_labels)

    # Announce final status
    if status_flag != None:
        if status_flag == 0:
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "Draw!")
        elif status_flag == 1:
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "O wins!")
        else:
            tkinter.messagebox.showinfo("Tic-Tac-Toe", "X wins!")
        init_game()

def is_game_over(board):
    global status_flag

    # Checking for draw
    draw_flag = True
    for i in range(3):
        if '' in board[i]:
            draw_flag = False
            break
    status_flag = 0 if draw_flag else None

    # Checking for row winning
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            if board[i][0] == 'X':
                status_flag = -1
            else:
                status_flag = 1
    
    # Checking for column winning
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != '':
            if board[0][j] == 'X':
                status_flag = -1
            else:
                status_flag = 1
    
    # Checking for top-right to down-left diagonal winning
    if board[0][0] == board[1][1] == board[2][2] != '':
        if board[0][0] == 'X':
            status_flag = -1
        else:
            status_flag = 1

    # Checking for top-left to down-right diagonal winning 
    elif board[0][2] == board[1][1] == board[2][0] != '':
        if board[2][0] == 'X':
            status_flag = -1
        else:
            status_flag = 1
    
    return status_flag

    
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


# The maximizer always plays as O and the minimzer as X
class Node:
    def __init__(self, board, is_maximizer):
        self.board = board
        self.is_maximizer = is_maximizer
        if is_maximizer:
            self.icon = "O"
            self.evalfunc = self.calculate_h('O') - self.calculate_h('X')
        else:
            self.icon = "X"
            self.evalfunc = self.calculate_h('X') - self.calculate_h('O')
        self.successors = None
        self.utilityfunc = self.calculate_utilityfunc()
        

    def calculate_h(self, icon):
        evalfunc = 0

        # Checking for row
        for i in range(3):
            flag = True
            for j in range(3):
                if self.board[i][j] == icon:
                    flag = False
                    break
            evalfunc = evalfunc+1 if flag else evalfunc

        # Checking for column
        for i in range(3):
            flag = True
            for j in range(3):
                if self.board[j][i] == icon:
                    flag = False
                    break
            evalfunc = evalfunc+1 if flag else evalfunc
        
        # Checking for top-right to down-left diagonal winning
        flag = True
        if self.board[0][0] == icon or  self.board[1][1] == icon or self.board[2][2] == icon:
            flag = False
        evalfunc = evalfunc+1 if flag else evalfunc

        # Checking for top-left to down-right diagonal winning 
        flag = True
        if self.board[0][2] == icon or  self.board[1][1] == icon or self.board[2][0] == icon:
            flag = False
        evalfunc = evalfunc+1 if flag else evalfunc
        
        return evalfunc


    def expand(self):
        successors = []
        for i in range(3):
            for j in range(3):
                if(self.board[i][j] == ''):
                    tmp = copy.deepcopy(self.board)
                    tmp[i][j] = self.icon
                    successors.append({"node" :Node(tmp, not self.is_maximizer), "action" : [i,j]})
        self.successors = successors
    
    def calculate_utilityfunc(self):
        status_flag = None

        # Checking for draw
        draw_flag = True
        for i in range(3):
            if '' in self.board[i]:
                draw_flag = False
                break
        status_flag = 0 if draw_flag else None


        # Checking for row winning
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                if self.board[i][0] == 'X':
                    status_flag = -1
                else:
                    status_flag = 1
        
        # Checking for column winning
        for j in range(3):
            if self.board[0][j] == self.board[1][j] == self.board[2][j] != '':
                if self.board[0][j] == 'X':
                    status_flag = -1
                else:
                    status_flag = 1
        
        # Checking for top-right to down-left diagonal winning
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            if self.board[0][0] == 'X':
                status_flag = -1
            else:
                status_flag = 1

        # Checking for top-left to down-right diagonal winning 
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            if self.board[0][2] == 'X':
                status_flag = -1
            else:
                status_flag = 1
        
        return status_flag
    
    def __str__(self):
        return str(self.board) + "   h=" + str(self.evalfunc)

def alpha_beta_search(node, i, j):
    v = max_value(node, -float('inf'), float('inf'))
    node.expand()
    return v['action']


def max_value(node, alpha, beta):
    # Terminal testing
    action = None
    if node.utilityfunc != None:
        return {"v":node.utilityfunc, "action": action}
    v = -float('inf')
    node.expand()
    for n in node.successors:
        min_value_child = min_value(n['node'], alpha, beta)['v']
        if v < min_value_child:
            v = min_value_child
            action = [n['action'][0],n['action'][1]]
        if v >= beta:
            return {"v":v, "action": action}
        alpha = max([alpha, v])
    return {"v":v, "action": action}

def min_value(node, alpha, beta):
    # Terminal testing
    action = None
    if node.utilityfunc != None:
        return {"v":node.utilityfunc, "action": action}
    v = float('inf')
    node.expand()
    for n in node.successors:
        max_value_child = max_value(n['node'], alpha, beta)['v']
        if v > max_value_child:
            v = max_value_child
            action = [n['action'][0],n['action'][1]]
        if v <= alpha:
            return {"v":v, "action": action}
        beta = min([beta, v])
    return {"v":v, "action": action}





init_game()
screen.mainloop()
s = Node([['X','O','X'], ['O','O','X'], ['O','X','X']], True)

