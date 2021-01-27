import tkinter as tk
import tkinter.messagebox
screen = tk.Tk()
screen.title("Tic Tac Toe")
screen.geometry("450x530")
screen.resizable(0, 0)

photo_x = tk.PhotoImage(file="./images/x.png")
photo_o = tk.PhotoImage(file="./images/o.png")


board = [["" for _ in range(3)] for _ in range(3)]


playter = True
flag = 0

def disableButton():
    for i in range(3):
        for j in range(3):
            board[i][j].configure(state=tk.DISABLED)




def btnClick(i, j):
    global playter, flag, board
    print(str(i) + str(j) + str(board[i][j]['text']) + str(playter))
    if not board[i][j]['text'] and playter == True:
        board[i][j].config(image=photo_x,width="145",height="153", bg="#67D7A4", activebackground ="#469871" )
        playter = False
        board[i][j]['text'] = 'x'
        update_label()
        flag += 1


    elif not board[i][j]['text'] and playter == False:
        board[i][j].config(image=photo_o,width="145",height="153", bg="#82DCE3", activebackground ="#66AEB5" )
        playter = True
        board[i][j]['text'] = 'o'
        update_label()
        flag += 1
    else:
        tkinter.messagebox.showinfo("Tic-Tac-Toe", "Button already Clicked!")

def refresh():
    for i in range(3):
        for j in range(3):
            board[i][j]['text']=''
            board[i][j]=tk.Button(text='',width=18,height=9, padx=0, pady = 0,command=lambda r=i,c=j: btnClick(r,c))
            board[i][j].grid(row=i,column=j)


def update_label():
    label_1=tk.Label(text="{}'s turn".format("X" if playter else "O"),font=('normal',18,'bold'), bg='#fff')
    label_1.grid(row=4,column=2)


for i in range(3):
    for j in range(3):
        board[i][j]=tk.Button(text='',width=18,height=9, padx=0, pady = 0,command=lambda r=i,c=j: btnClick(r,c))
        board[i][j].grid(row=i,column=j)


screen.mainloop()