
import random
import time
import tkinter as tk
from tkinter import font
from tkinter import ttk
import json
import os
import numpy as np
os.chdir("C://Users\Wei Yang\Desktop\SUTD\CTD\CTD 1D\CTD-1D-Project-main")

class TyperacerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Typeracer Game")

        self.words = ["python", "programming", "challenge", "typeracer", "keyboard", "developer", "coding", "practice", "speed", "game"]
        self.current_word = ""
        self.user_input = ""
        self.score = 0
        self.time_start = 0
        self.timer_running = False

        self.word_label = tk.Label(root, text="", font=("Helvetica", 24))
        self.word_label.pack(pady=30)

        self.entry = tk.Entry(root, font=("Helvetica", 18))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.check_input)

        self.score_label = tk.Label(root, text="Score: 0", font=("Helvetica", 18))
        self.score_label.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        self.score = 0
        self.update_score()
        self.start_new_word()
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        self.timer_running = True
        self.time_start = time.time()
        self.update_timer()

    def update_score(self):
        self.score_label.config(text="Score: {}".format(self.score))

    def start_new_word(self):
        self.current_word = random.choice(self.words)
        self.word_label.config(text=self.current_word)

    def check_input(self, event):
        if self.timer_running:
            self.user_input = self.entry.get().strip()
            if self.user_input == self.current_word:
                self.score += 1
                self.update_score()
                self.start_new_word()
                self.entry.delete(0, tk.END)

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.time_start)
            self.root.after(1000, self.update_timer)
            self.root.title("Typeracer Game - Time: {}s".format(elapsed_time))
            if elapsed_time >= 30:
                self.timer_running = False
                self.root.title("Typeracer Game - Time's up!")
                self.entry.delete(0, tk.END)
                self.entry.unbind("<Return>")
                self.start_button.config(state=tk.NORMAL)

class Level:
    def __init__(self,lvl,special =False) :
        self.lvl_num = lvl
        self.list_of_enemies = []
        self.event = special
        f = open('Enemy.json')
        self.enemyjson = json.load(f)['enemy_details']

    def get_level(self):
        return self.lvl_num+1
    
    def get_list_of_enemies(self):
        return self.list_of_enemies

    def generate_lvl(self):
        if self.event == False:
            
            NumOfEnemies = int(2+abs(1+self.lvl_num)*.4)
            temp = random.sample(self.enemyjson,3)
            for i in temp:
                self.list_of_enemies.append(enemy(enemyname=i['enemy_name'],enemyhp=i['enemy_health'],enemyimage=i['enemy_pic_name'],damage= i['enemy_damage'],cooldown = 0)) # remeber to change damage and cooldown

            
            self.LvlUp()
            return self
        elif self.event== True:
            pass

    def LvlUp(self):
        temp =[]
        for i in self.list_of_enemies:

            temp.append(i.set_Lvl(self.lvl_num))
        self.list_of_enemies = temp
        
    def Choose_Enemy(self):
        return random.sample(self.list_of_enemies,1)[0]
    
    
class enemy:
    def __init__(self,enemyname,enemyhp,enemyimage, dialogue= '',EXP= 0,damage= 0,cooldown = 0):

        self.enemyhp =enemyhp
        self.enemyimage=enemyimage
        self.enemyname=enemyname
        self.EXP = EXP
        self.dialogue =dialogue
        self.damage =damage
        self.cooldown =cooldown
    def gethealth(self):
        ###Everyword typed, check for hp###
        return self.enemyhp
    def getname(self):
        return self.enemyname   
    def getimage(self):
        return self.enemyimage
        
    
    def sethealth(self,value):
        self.enemyhp += value


    def getEXP(self,player_lvl=None,lvl=None):
        return self.EXP
    
    def set_Lvl(self,lvl):
        self.enemyhp =  int(self.enemyhp*np.log(self.enemyhp+lvl*1.2))
        self.damage =int(self.damage*np.log(self.damage+lvl*1.2))
        self.cooldown = int(self.cooldown- 2*np.log2((lvl+1)*.9))
        return self


    
def create_MainMenu_window():
    
    Frame = ttk.Frame(window)
    #START
    window.title("TEST ALPHA")  
    #Declare Widgits
    Blank = ttk.Label(Frame,text='',width=45)
    Blank2 = ttk.Label(Frame,text='',width=10)

    Title = tk.Label(Frame,text='Type Caster',font=("Comfortaa",40))
    PlayButton = tk.Button(Frame,text='Play',command =lambda:start_game() )
    #Grid Method
    Title.grid(row=0,column=1)
    PlayButton.grid(row = 1, column = 1)
    Frame.grid(row=0,column=0)
    #Blank.grid(row=0,column=0) 
    #Blank2.grid(row=1,column=0)
def start_game():
    Levels.append(Level(Current_Level).generate_lvl())
    
    game_page()

def game_page(): 
    
    def NextEnemy(widget,container,lvl):
        global Current_Level
        #Update Level list and Selected Enemy------------------------------------
        Current_Level +=1
        Levels.append(Level(Current_Level).generate_lvl())
        enemy = Levels[-1].Choose_Enemy()

        # Update GUI-----------------------------------------------
        img =tk.PhotoImage(file="assets/images/"+enemy.getimage())
        Frame.img =img 
        widget.itemconfig(container,image=img) 
        Enemy_info.config(text='  Name: {Name}'.format(Name=enemy.getname()).ljust(17)+'Health: {health}'.format(health=enemy.gethealth()).ljust(12),relief="solid")
        
    enemy = Levels[Current_Level-1].Choose_Enemy()
    print(enemy)
    style =ttk.Style()
    Font =font.Font(family = 'MS Gothic')
    style.configure('TFrame', background='black')
    style.configure('TLabel',background='black',font=Font,foreground='white')

    
    #Declare Widgits-----------------------------------------------
    #FRAMES----------------------------------------------
    Frame = ttk.Frame(window,style='TFrame')
    Left_block = ttk.Frame(Frame,width=200,height=300,relief="solid")
    Mid_block= ttk.Frame(Frame,width=200,height=300,relief="solid")
    Right_block = ttk.Frame(Frame,width=200,height=300,relief="solid")
    
#----------------------------------------------------------------------
    settings_button = tk.Button(Frame, text = "Next", width=30, borderwidth=2, relief="raised",command=lambda:NextEnemy(Enemy_canvas,container,Current_Level+1)) #Add setting menu, Currently randomise picture
    Enemy_canvas =tk.Canvas(Mid_block,width=200,height=300,bg='black')
    
    Enemy_info = ttk.Label(Frame,text='  Name: {Name}'.format(Name=enemy.getname()).ljust(17)+'Health: {health}'.format(health=enemy.gethealth()).ljust(12),relief="solid") #Call method get_health and get_name for format
    Player_info = ttk.Label(Frame, text = '  Name: {Name}'.format(Name='Player').ljust(17)+'Health: {health}'.format(health='100').ljust(12), borderwidth=2, relief="solid") #Call method get_health and get_name for format
    Word_box = ttk.Frame(Frame,width=200,height=45,relief="solid",padding=10)
    Entry = ttk.Entry(Frame,width=30)

    Word_request = ttk.Label(Word_box,text='TESTING')
    #Grid Method-----------------------------------------------
    Left_block.grid(row=0,column=0,padx=3,pady=5) 
    Right_block.grid(row=0,column=3,padx=3,pady=5)
    Mid_block.grid(row=0,column=1,padx=3,pady=5)
    Mid_block.grid_propagate (False) 
    Enemy_info.grid(row=1,column=1,pady=5)
    Enemy_canvas.grid(row = 0, column = 0, sticky = tk.W, pady = 2)
    settings_button.grid(row = 1,column = 3)
    Player_info.grid(row=3,column=1,pady=5)
    Entry.grid(row=5,column=1,pady=20)
    Word_box.grid(row=4,column=1,pady=5)
    Word_box.grid_propagate (False) 
    Word_request.place(relx=0.5, rely=0.5, anchor="center")
    Frame.grid(row=0,column=0, sticky=(tk.W,tk.E,tk.N,tk.S))


    #add image
    img =tk.PhotoImage(file="assets/images/"+enemy.getimage())
    Frame.img =img 
    container = Enemy_canvas.create_image(0,0,image=img,anchor='nw') 
    


Levels = []
if __name__ == "__main__":
    Current_Level = 1
    window = tk.Tk()
    create_MainMenu_window()
    #game_page(window)        
    tk.mainloop()
        