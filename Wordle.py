import tkinter as tk
import random
import pygame

GOOD_SOUND = "FILE NAME HERE"
FAIL_SOUND = "FILE NAME HERE"
font = ("Franklin Gothic Demi", 10)



class Wordle:
    def __init__(self, fileName):
        
        pygame.mixer.init()
        with open(fileName) as f:
            lines = f.readlines()
            self.chosen_word = [random.choice(lines).strip().upper()]

        self.window = tk.Tk()
        self.window.title("Wordle")
        self.window.geometry("640x640")

        self.row_borders = [[tk.LabelFrame(self.window, background="grey", relief="flat", bd=1) for i in range(5)] for j in range(6)]
        self.rows = [[tk.Label(self.row_borders[j][i], text="", bd=0, width=6, height=3, justify="center", font=font) for i in range(5)] for j in range(6)]

        for j in range(6):
    
            for i in range(5):
       
                self.rows[j][i].grid(row=0, column=3+j, padx=1, pady=1, sticky='')
                self.row_borders[j][i].grid(row=j, column=i+3, padx=3, pady=2, sticky='')


        self.buttons = [[], [], []]
        self.letter_list = ["Q","W","E","R","T","Y","U","I","O","P","A","S","D","F","G","H","J","K","L","ENTER","Z","X","C","V","B","N","M", "⌫"]


        for l in range(len(self.letter_list)):
            if l <= 9:
               self.buttons[0].append(tk.Button(self.window, text=self.letter_list[l], command=lambda x=self.letter_list[l]: self.buttonPressed(x), relief="flat", bg="light grey", width=5, height=3, bd=0, font=font))
               self.buttons[0][-1].grid(row=10, column=l+1, padx=3, pady=4, sticky='e')
     
            elif l >= 19:
               self.buttons[2].append(tk.Button(self.window, text=self.letter_list[l], command=lambda x=self.letter_list[l]: self.buttonPressed(x), relief="flat", bg="light grey", width=5, height=3, bd=0, font=font))
               self.buttons[2][-1].grid(row=12, column=l%19+2, padx=3, pady=4, sticky='e')
       
            else:
               self.buttons[1].append(tk.Button(self.window, text=self.letter_list[l], command=lambda x=self.letter_list[l]: self.buttonPressed(x), relief="flat", bg="light grey", width=5, height=3, bd=0, font=font))
               self.buttons[1][-1].grid(row=11, column=l%10 +2, padx=3, pady=4, sticky='e')



        self.padding = tk.Label(self.window)
        self.padding.grid(row=10, column=0, padx=20)


        self.play_button = tk.Button(self.window, text="Continue", relief="flat", bd=2, command=lambda x=self.chosen_word: self.reset(x), font=font, bg="grey", width=10, height=3, state="disabled", fg="white")
        self.play_button.grid(row=0, column=11, pady=2)


        self.quit_button = tk.Button(self.window, text="Quit", relief="flat", bd=2, command=self.window.quit, font=font, bg="grey", width=10, height=3)
        self.quit_button.grid(row=1, column=11, pady=2)

        self.streak = tk.Label(self.window, background="goldenrod", relief="flat", bd=1, text=f"Streak: 0", width=10, height=3, font=font, fg="white")
        self.streak.grid(row=2, column=11, pady=2)

        self.idx = 0
        self.current = ""
        self.letters = [set([]), set([])]
        self.score = 0



    def keyToChar(self, event):
        self.buttonPressed(event.keysym.upper())
   


    def buttonPressed(self, letter):

        if self.idx >= 6:
            return
    

        if len(self.current) < 5 and letter.isalpha() and len(letter) == 1:
            self.current += letter
            self.rows[self.idx][len(self.current) - 1].config(text=letter)
        
        
        elif len(self.current) > 0 and (letter == "⌫" or letter == "BACKSPACE"):
            self.rows[self.idx][len(self.current) - 1].config(text="")
            self.current = self.current[:len(self.current) - 1]
        
        elif len(self.current) == 5 and (letter == "ENTER" or letter == "RETURN"):
           
            for c in range(len(self.current)):
                y,x = self.letterNumMap(self.current[c])

                if self.current[c] == self.chosen_word[0][c]:
                    self.rows[self.idx][c].config(fg="white", bg="SpringGreen4")
                    self.row_borders[self.idx][c].config(bg="SpringGreen4")
                    self.buttons[y][x].config(bg="SpringGreen4", fg="white")
                    self.letters[1].add(self.current[c])
                
                elif self.current[c] in set([w for w in self.chosen_word[0]]):
                    self.rows[self.idx][c].config(fg="white", bg="goldenrod")
                    self.row_borders[self.idx][c].config(bg="goldenrod")
                    self.letters[0].add(self.current[c])
                    if not (self.current[c] in self.letters[1]): 
                        self.buttons[y][x].config(bg="goldenrod", fg="white")
                
                else:
                    self.rows[self.idx][c].config(fg="white", bg="dark grey")
                    self.row_borders[self.idx][c].config(bg="dark grey")
                    if not (self.current[c] in self.letters[0]):
                        self.buttons[y][x].config(bg="dark grey", fg="white")
                    
            
        
            self.idx += 1
            if self.current == self.chosen_word[0] or self.idx == 6:
            
                self.result_screen(self.current == self.chosen_word[0])
            
            
            self.current = ""
        
         

    
    def letterNumMap(self, letter):
     
        if (idx := self.letter_list.index(letter)) <= 9:
            return (0, idx)
        elif idx >= 19:
            return (2, idx % 19)
    
        return (1, idx % 10)
    


    def reset(self, chosen_word):
        self.streak.config(bg="goldenrod")
        for r in range(len(self.rows)):
            for col in range(len(self.rows[r])):
                self.rows[r][col].config(text="", bg="white", fg="black")
                self.row_borders[r][col].config(bg="grey")
     
        for row in range(3):
            for r in range(len(self.buttons[row])):
                self.buttons[row][r].config(bg="light grey", fg="black")
            
        self.play_button.config(state="disabled", bg="grey")
        with open("f.txt") as f:
            lines = f.readlines()
            chosen_word[0] = random.choice(lines).strip().upper()
        

        self.idx = 0
        self.current = ""
        self.letters = [set([]), set([])]
        


    def result_screen(self, guesses):
        
        self.play_button.config(state="normal", bg="springgreen4")
    
        if guesses == True:
            self.score += 1
            pygame.mixer.music.load(GOOD_SOUND)
            self.streak.config(bg="darkgoldenrod1")

        else:
            self.score = 0      
            self.streak.config(bg="brown3")
            pygame.mixer.music.load(FAIL_SOUND)
            

    
        self.streak.config(text=f"Streak: {self.score}")
        pygame.mixer.music.play()
        


    def run_game(self):
        self.window.bind('<KeyPress>', self.keyToChar)
        self.window.mainloop()


w = Wordle("WORD LIST FILE")
w.run_game()
