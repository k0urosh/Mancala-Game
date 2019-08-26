import tkinter as tk
import Mancala
import GameAI
import math
import copy

class Home:
    def __init__(self, root):
        self.root = root
        # place frame into root
        self.frame = tk.Frame(root)
        self.frame.grid()
        
        label_column = tk.Label(self.frame, text="Columns")
        label_seed = tk.Label(self.frame, text="Seed")
        label_column.config(font=('helvetica', 12, 'bold'))
        label_seed.config(font=('helvetica', 12, 'bold'))
        # textbox for player to enter values
        self.entry_column = tk.Entry(self.frame)
        self.entry_seed = tk.Entry(self.frame)
        self.entry_column.config(font=('helvetica', 12))
        self.entry_seed.config(font=('helvetica', 12))
        
        # textbox for player to enter names
        label_p1 = tk.Label(self.frame, text="Player 1 name")
        label_p2 = tk.Label(self.frame, text="Player 2 name")
        label_p1.config(font=('helvetica', 12, 'bold'))
        label_p2.config(font=('helvetica', 12, 'bold'))
        self.entry_p1_name = tk.Entry(self.frame)
        self.entry_p2_name = tk.Entry(self.frame)
        self.entry_p1_name.config(font=('helvetica', 12))
        self.entry_p2_name.config(font=('helvetica', 12))
        label_p1.grid(row=2, column=0)
        label_p2.grid(row=3,column=0)
               
        # create radio buttons
        self.entry_ai = tk.IntVar()
        label_ai = tk.Label(self.frame, text="AI")
        label_ai.config(font=('helvetica', 12, 'bold'))
        rb1 = tk.Radiobutton(self.frame, text="Yes", variable=self.entry_ai, value=1)
        rb2 = tk.Radiobutton(self.frame, text="No", variable=self.entry_ai, value=0)
        rb1.config(font=('helvetica', 12, 'bold'))
        rb2.config(font=('helvetica', 12, 'bold'))
        rb1.bind("<Button-1>", self.enable_or_disable_entry)
        rb2.bind("<Button-1>", self.enable_or_disable_entry)
        
        self.submit_button = tk.Button(self.frame, text="Submit")
        self.submit_button.bind("<Button-1>", self.submit)
        self.submit_button.config(font=('helvetica', 12, 'bold'))
        
        # displaying
        label_column.grid(row=0, column=0)
        label_seed.grid(row=1, column=0)
        self.entry_column.grid(row=0, column=1, columnspan=2)
        self.entry_seed.grid(row=1, column=1, columnspan=2)
        self.entry_p1_name.grid(row=2, column=1, columnspan=2)
        self.entry_p2_name.grid(row=3, column=1, columnspan=2)
        label_ai.grid(row=4, column=0)
        rb1.grid(row=4, column=1)
        rb2.grid(row=4, column=2)
        self.submit_button.grid(row=5, column=1, columnspan=2)

    # checks whether all info is filled before going to the next gui.
    def submit(self, event):     
        flag = False     
        # message box prompts the user error/warning
        if self.entry_seed.get().isdigit() == False or self.entry_column.get().isdigit() == False:
            tk.messagebox.showinfo("Warning", "Enter numbers not alphabets")
            flag = True
        else:
            if len(self.entry_seed.get())==0 or len(self.entry_column.get())==0 or len(self.entry_p1_name.get())==0 or len(self.entry_p2_name.get())==0:
                tk.messagebox.showinfo("Warning", "Fill in all the blanks")
                flag = True            
            if len(self.entry_column.get())!=0 and int(self.entry_column.get()) < 4:
                tk.messagebox.showinfo("Warning", "Enter columns greater than 3")
                flag = True
            if len(self.entry_seed.get())!=0 and int(self.entry_seed.get()) < 1:
                tk.messagebox.showinfo("Warning", "Enter seed greater than 0")
                flag = True 
                   
        if flag == False:     
            name1 = self.entry_p1_name.get()
            if int(self.entry_ai.get()) == 0:
                name2 = self.entry_p2_name.get()
            else:
                name2 = "AI"
                        
            d = Mancala.Mancala(int(self.entry_column.get()), int(self.entry_seed.get()), name1, name2)
            
            temp = int(self.entry_ai.get())
            self.frame.destroy()
            Game(self.root, d, temp)

    # if ai radio button "yes" is chosen, disabled player 2 name from being entered, vice versa
    def enable_or_disable_entry(self, event):
        if int(self.entry_ai.get())== 0:
            self.entry_p2_name.delete(0, tk.END)
            self.entry_p2_name.insert(tk.END, " ")
            self.entry_p2_name.config(state=tk.DISABLED)
        else:
            self.entry_p2_name.config(state=tk.NORMAL)
            self.entry_p2_name.delete(0, tk.END)
            
              
class Game:
    # pass some values from previous form, to the current form
    def __init__(self, root, game, ai):
        self.ai = ai
        self.bList = []
        self.game = game
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.grid()              
        
        #create and display buttons for the game board
        z=0
        for x in range (int(len(self.game.board.board)/2)-1, -1, -1):
            b = tk.Button(self.frame, text = str(self.game.board.board[x]), height = 3, width = 6)
            b['command'] = lambda arg = x : self.buttonAction(arg)
            b.config(font=('helvetica', 20, 'bold'))
            b.grid(row=1, column=z)
            z=z+1
            self.bList.insert(0,b)
            
        #create and display buttons for the game board
        z=0
        for y in range(int(len(self.game.board.board)/2), int(len(self.game.board.board))):
            b = tk.Button(self.frame, text = str(self.game.board.board[y]), height = 3, width = 6)
            b['command'] = lambda arg = y : self.buttonAction(arg)
            b.config(font=('helvetica', 20, 'bold'))
            b.grid(row=2, column=z)
            z=z+1
            self.bList.append(b)
            
        # display player score
        self.label_p1 = tk.Label(self.frame, text=self.game.p1.name + ": " + str(self.game.p1.score))
        self.label_p2 = tk.Label(self.frame, text=self.game.p2.name + ": " + str(self.game.p2.score))
        self.label_p1.config(font=('helvetica', 12, 'bold'))
        self.label_p2.config(font=('helvetica', 12, 'bold'))
        self.label_p1.grid(row=4, columnspan=int(len(self.game.board.board)/2))
        self.label_p2.grid(row=5, columnspan=int(len(self.game.board.board)/2))
  
        self.label_top = tk.Label(self.frame, text="<---------------  " + self.game.p1.name + "  <---------------")
        self.label_btm = tk.Label(self.frame, text="--------------->  " + self.game.p2.name + "  --------------->")
        self.label_top.config(font=('helvetica', 14, 'bold'))
        self.label_btm.config(font=('helvetica', 14, 'bold'))
        self.label_top.grid(row=0, columnspan=int(len(self.game.board.board)/2))
        self.label_btm.grid(row=3, columnspan=int(len(self.game.board.board)/2))
        
        # display turn and any wrong moves
        self.label_who = tk.Label(self.frame, text=self.game.p1.name + "'s turn", bd=1)
        self.label_who.config(font=('helvetica', 14, 'bold'))
        self.label_who.grid(row=6, columnspan=int(len(self.game.board.board)/2))

    # what the buttons for the gameboard does.
    # basically get the row and col of the button, convert it into 1D array value. 
    # pass the value into self.checkMove(), call the updateGUI and end the game if needed.
    def buttonAction(self, arg):
        self.checkMove(arg)
        self.updateGUI()
        
        if(self.game.checkGameState() == False):
            self.frame.destroy()
            End(self.root, self.game)
                           
    # updates GUI    
    def updateGUI(self):
        #updates button for gameboard
        for x in range(0, int(len(self.game.board.board))):            
            self.bList[x].config(text=str(self.game.board.board[x])) 
            
        # update score
        self.label_p1.config(text=self.game.p1.name + ": " + str(self.game.p1.score))
        self.label_p2.config(text=self.game.p2.name + ": " + str(self.game.p2.score))
        
        # update who's turn currently
        if(self.game.turn == False):
            string = self.game.p2.name + "'s turn"
        else:
            string = self.game.p1.name + "'s turn"
        self.label_who.config(text=string + self.status)
        
    # check move made if it is valid
    # valid = own side of board and seed is not 0
    # will also call the AI after player has made its move
    def checkMove(self, move):
        self.status = ""
        if self.game.turn == True:
            for i in range (0, int(len(self.game.board.board)/2)):
                if i == move and self.game.board.board[i] != 0:
                    seed = self.game.board.board[move]
                    self.disable(0)
                    self.updateBoard(move, seed, 1)                   
                    return
        else:
            for i in range (int(len(self.game.board.board)/2), len(self.game.board.board)):               
                if i == move and self.game.board.board[i] != 0:  
                    seed = self.game.board.board[move]
                    self.disable(0)
                    self.updateBoard(move, seed, 1)                                    
                    return
        self.status = " - invalid move"
     
    # update board in the Model, (mancala class)
    def updateBoard(self, move, seed, count):
        # place seed in a temporary variable and set seed at chosen move to 0.     
        i = move
        if count == 1:
            self.game.board.board[move] = 0            
            count = count - 1
        
        # loop until the seed left from the taken hole = 0
        if seed < 0:
            return
        if seed > 0:
            if(i+1 < len(self.game.board.board)):
                i = i + 1
            else:
                i = 0            
            self.game.board.board[i] = self.game.board.board[i] + 1
            abc = seed - 1
            self.updateGUI()
            self.root.after(500, lambda: self.updateBoard(i, abc, count))
            return True
        
        if seed == 0:
            if i+1 == len(self.game.board.board):
                x = 0
            else:
                x = i+1
            # if the next hole not empty, call updateBoard again.
            if self.game.board.board[x] != 0:
                abc = self.game.board.board[x]
                self.root.after(500, lambda: self.updateBoard(x, abc, 1))
                
            else:
                # if it is empty, place the value of the seed to the current player's score
                # then empty the hole
                if x+1 == len(self.game.board.board):
                    x = 0
                else:
                    x = x + 1
                if self.game.turn == True:
                    self.game.p1.score = self.game.p1.score + self.game.board.board[x]
                else:
                    self.game.p2.score = self.game.p2.score + self.game.board.board[x]
                self.game.board.board[x] = 0               
                self.changeTurn()
                self.updateGUI()
                self.disable(1)
                self.get_AI_Move()
                            
    def changeTurn(self):
        if self.game.turn == False:
            self.game.turn = True
        else:
            self.game.turn = False
            
    def get_AI_Move(self):
        if(self.ai == 1):
            a = GameAI.AI(copy.copy(self.game.board.board), False)
            a.alphaBeta(copy.copy(self.game.board.board), -math.inf, math.inf, 3, True)                     
            self.checkMove(a.move)
            
            if(self.game.checkGameState() == False):
                self.frame.destroy()
                End(self.root, self.game)
                
    def disable(self, val):
        for b in self.bList:
            if val == 0:
                b.configure(state=tk.DISABLED)               
            else:
                b.configure(state=tk.NORMAL)
        
class End:
    def __init__(self, root, game):
        self.game = game
        self.root = root
        self.frame = tk.Frame(self.root)
        self.frame.grid()
        self.announce = tk.Label(self.frame)
        self.announce.config(font=('helvetica', 14, 'bold'))
        self.announce.grid(row=0, columnspan=2)
        if(self.game.p1.score > self.game.p2.score):
            self.announce.config(text=self.game.p1.name + " wins!")
        elif(self.game.p1.score < self.game.p2.score):
            self.announce.config(text=self.game.p2.name + " wins!")
        else:
            self.announce.config(text="Draw!")
        
        
        self.label_p1 = tk.Label(self.frame, text=self.game.p1.name + ": " + str(self.game.p1.score))
        self.label_p2 = tk.Label(self.frame, text=self.game.p2.name + ": " + str(self.game.p2.score))
        self.label_p1.config(font=('helvetica', 14, 'bold'))
        self.label_p2.config(font=('helvetica', 14, 'bold'))
        self.label_p1.grid(row=1, columnspan=2)
        self.label_p2.grid(row=2, columnspan=2)
        
        self.label3 = tk.Label(self.frame, text="Play again?")
        self.label3.config(font=('helvetica', 14, 'bold'))
        self.label3.grid(row=3, columnspan=2)
        
        self.button_yes = tk.Button(self.frame, text="Yes", command=self.yes, width=12)
        self.button_no = tk.Button(self.frame, text="No", command=self.no, width=12)  
        self.button_yes.config(font=('helvetica', 14, 'bold'))
        self.button_no.config(font=('helvetica', 14, 'bold'))
        self.button_yes.grid(row=4, column=0)
        self.button_no.grid(row=4, column=1)
        
    def no(self):
        self.root.destroy()
        
    def yes(self):
        self.root.destroy()
        root = tk.Tk()  
        root.title("Mancala")   
        Home(root)
        root.mainloop()











