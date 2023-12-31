# -*- coding: utf-8 -*-

"--*-- IMPORTS --*--"

import sys
import datetime as dt
from tkinter import *
from math import pi, sin, cos, e, sqrt, floor, ceil
from random import random, randint, choice
from time import sleep, process_time
from os import chdir
from pickle import *

if 'win' in sys.platform:
    from winsound import *
    play_sound = lambda sound: PlaySound(sound, SND_FILENAME)

else:
    try:
        import playsound
    except ImportError:
        import pip
        pip.main(["install", "playsound"])
        import playsound
    finally:
        play_sound = lambda sound: playsound.playsound(sound)

#Screen Resolution#
import ctypes
user32 = ctypes.windll.user32
w,h = (user32.GetSystemMetrics(0),
       user32.GetSystemMetrics(1))
#Screen Resolution#

class Menu:

    def __init__(menu):
        menu.ignite()

        menu.TITLE_img  = PhotoImage(master=menu.root,file='./assets/titulo.gif')
        menu.PLAY_img   = PhotoImage(master=menu.root,file='./assets/Play2.gif')
        menu.EXIT_img   = PhotoImage(master=menu.root,file='./assets/Exit2.gif')
        menu.RANK_img   = PhotoImage(master=menu.root,file='./assets/Ranking2.gif')
        menu.BACK_img   = PhotoImage(master=menu.root,file='./assets/BacktoMenu.gif')
        menu.CNTRLS_img = PhotoImage(master=menu.root,file='./assets/Controls.gif')
        menu.INTRO_img  = PhotoImage(master=menu.root,file='./assets/A_long_time_ago.gif')
        
        menu.introduce()
        menu.root.after(3500, menu.mount)

        menu.ranking = Ranking()

        menu.root.mainloop()

    def introduce(menu):
        menu.Intro = Label(menu.root,image=menu.INTRO_img,bd=0)
        menu.Intro.pack(anchor='center')

        #thread.start_new_thread(menu._PlayTheme,())

    def _PlayTheme(menu):
        while True:
            play_sound("./assets/main_theme.wav")

    def ignite(menu):
        """
        Show Menu.
        """
        menu.root = Tk()
        menu.root.geometry("%ix%i+0+0" %(w,h))
        menu.root.attributes("-fullscreen", True)
        menu.root.configure(background='black')

    def mount(menu):
        menu.Intro.pack_forget()

        "<><><><><><><><><><>"
        menu.TITLE_lbl = Label(menu.root,bg='black',image=menu.TITLE_img,height=210,bd=0)
        menu.TITLE_lbl.pack(side='top')
        "<><><><><><><><><><>"
#        menu.BUTTON_FRAME = Frame(menu.root, height=50, bg='black')
#        menu.BUTTON_FRAME.pack()
        "<><><><><><><><><><>"
        menu.PLAY_btn = Label(menu.root,bg='black', image=menu.PLAY_img,height=90,bd=0)
        menu.PLAY_btn.pack()
        menu.PLAY_btn.bind("<ButtonPress-1><ButtonRelease-1>", menu._play)
        "<><><><><><><><><><>"
        menu.RANK_btn = Label(menu.root, image=menu.RANK_img,height=90,bg='black',bd=0)
        menu.RANK_btn.pack()
        menu.RANK_btn.bind("<ButtonPress-1><ButtonRelease-1>", menu._rank)
        "<><><><><><><><><><>"
        menu.EXIT_btn = Label(menu.root, bg='black', image=menu.EXIT_img,height=90,bd=0)
        menu.EXIT_btn.pack()
        menu.EXIT_btn.bind("<ButtonPress-1><ButtonRelease-1>", menu._exit)
        "<><><><><><><><><><>"
        menu.BACK_btn = Label(menu.root, bg='black', image = menu.BACK_img,height=150,bd=0)
        menu.BACK_btn.pack_forget()
        menu.BACK_btn.bind("<ButtonPress-1><ButtonRelease-1>", menu._back)
        "<><><><><><><><><><>"
        menu.CNTRLS_lbl = Label(menu.root, image=menu.CNTRLS_img,bd=0)
        menu.CNTRLS_lbl.pack(side='bottom')
        "<><><><><><><><><><>"

    def _play(menu, event):
        menu.root.destroy()
        fase = Fase(menu,w,h)

    def _exit(menu, event):
        menu.root.destroy()
        
    def _rank(menu, event):
#        menu.BUTTON_FRAME.pack_forget()
        menu.PLAY_btn.pack_forget()
        menu.RANK_btn.pack_forget()
        menu.EXIT_btn.pack_forget()
        menu.CNTRLS_lbl.pack_forget()
        menu.BACK_btn.pack(side='bottom')
        menu.RECORDS = []
        menu.LABELS = Frame(menu.root,bg='black')
        menu.LABELS.pack()

        _format = "%5s -- %8d -- %2d/%2d/%2d\n"

        for name,pts,date in menu.ranking.list:
            record = (name,pts,date[0],date[1],date[2])
            label = Label(menu.LABELS, text=_format%record, bg='black',fg='white')
            label.pack()
            menu.RECORDS += [label]

    def _back(menu, event):
#        menu.BUTTON_FRAME.pack()
        menu.PLAY_btn.pack()
        menu.RANK_btn.pack()
        menu.EXIT_btn.pack()
        menu.CNTRLS_lbl.pack(side='bottom')
        menu.LABELS.pack_forget()
        menu.BACK_btn.pack_forget()
        
class Ranking(object):
    """
    Ranking has tuples with:
    [ (name, score, *date) ... ]
    """
    def __init__(rank):
        td = dt.datetime.today()
        rank.today = td.day, td.month, td.year
        del td
        
        try:
            _file = open("./assets/rank.dt","rb")
            rank.list = load(_file)
            _file.close()
        except:
            _file = open("./assets/rank.dt","wb").close()
            rank.list = list()
            
    def save(rank):
        "======================"
        _file = open("./assets/rank.dt","wb")
        dump(rank.list, _file)
        _file.close()
        "======================"

    def update(rank, name, pts):
        "======================"
        rank.list += [(name, pts, tuple(i for i in rank.today))]

        rank.list  = sorted(rank.list, key=lambda _tuple: _tuple[1],reverse=True)[:10]
        "======================"
        
    def __repr__(rank):
        string  = str()
        _format = "%5s -- %8d -- %2d/%2d/%2d\n"
        for name, pts, date in rank.list:
            string += _format %(name, pts, date[0], date[1], date[2])
        return string
    
class Fase:

    def __init__(fase, menu, *mapa):
        fase.menu = menu

        if len(mapa) != 2:
            mapa = (1000, 600)

        fase.contador = 0
        
        fase.xy = mapa[0], mapa[1]
        fase.x , fase.y = fase.xy

        fase.ignite()
        fase.loop()
        fase.root.mainloop()
        fase.flag = True

        
    def ignite(fase):
        """
        Start game
        """
        
        fase.root = Tk()
        
        fase.cosmos = Universe(fase.root, fase.x, fase.y, fase.menu)
        
        fase.root.title("Jogo")
        fase.root.geometry("%ix%i+0+0" %fase.xy)
        fase.root.attributes("-fullscreen", True)
        fase.root.config(cursor='none')
            

    def loop(fase):
        """
        Game loop
        """
        fase.contador+=1
        if fase.contador%int(64/fase.cosmos.nivel) == 0:
            fase.cosmos.Fighters.append(fase.cosmos.Space.create_image(fase.cosmos.LX*random(),0,
                image=fase.cosmos.FIGHTER_img))
                                  
        if fase.contador%choice([(i+1)*12 for i in range(fase.cosmos.nivel)]) == 0:
            MF_X = fase.cosmos.Space.coords(fase.cosmos.MF)[0]
            for atirador in fase.cosmos.Fighters:
                if abs(fase.cosmos.Space.coords(atirador)[0] - MF_X) <= fase.cosmos.nivel*10:  
                    fase.cosmos.fire_fighter(atirador) 
            
        if fase.contador%choice([80,40,20]) == 0:
            fase.cosmos.createAsteroid(randint(10, fase.x-10),0)

        for fighter in fase.cosmos.Fighters:
            fase.move_fighter(fighter)

            
        fase.root.after(fase.cosmos.LAPSO, fase.loop)
        
        
    def move_fighter(fase, fighter):
        """
        Move TIE fighters according to Millenium Falcon's coordinates
        """
        if fase.cosmos.Space.coords(fighter)[0]<fase.cosmos.Space.coords(fase.cosmos.MF)[0]:
            fase.cosmos.Space.move(fighter,2,7)
        elif fase.cosmos.Space.coords(fighter)[0]>=fase.cosmos.Space.coords(fase.cosmos.MF)[0]:
            fase.cosmos.Space.move(fighter,-2,7)

class Universe:

    def __init__(self, toplvl, x, y, menu):
        self.menu = menu
        
        self.LX, self.LY, = x, y
        self.stars = (x*y)/(x+y)

        self.time = process_time
        self.start = process_time()
        self.nivel=1

        self.root  = toplvl
        self.Space = Canvas(toplvl,width=x,height=y,bg='#000000')
        self.Space.pack(expand=True, fill='both')

        self.score = 0
        self.scoreboard = Label(self.Space, text = 'fighters: %d'%self.score,bg='#000000',
                                fg ='white',font=('arial',12))
        self.scoreboard.place(relx=0.9,rely=0.9)

        self.timeboard = Label(self.Space, text = "time: %.3f"%(process_time()-self.start) ,bg='#000000',
                                fg ='white',font=('arial',12))
        self.timeboard.place(relx=0.9,rely=0.95)

        self.askforname = Frame(self.Space)
        self.askforname.place_forget()
        
        self.question = Label(self.askforname, text = "Enter your name:",fg='white',bg='black')
        self.question.pack()

        self.p_name = StringVar()
        self.answer = Entry(self.askforname, textvariable=self.p_name)
        self.answer.pack()
        
        self.Stars = []
        self.Fighters=[]
        self.tirosrebeldes=[]
        self.tirosdoImperio=[]
               
        self.VEL = 3.5
        self.CONTAGEM = 0
        self.LAPSO = 5

        #===============================================#
        #               :: Movement ::                  #   
        toplvl.bind("<KeyPress-Left>"   ,self.a_left)   #   
        toplvl.bind("<KeyRelease-Left>" ,self.d_left)   #   
                                                        #   
        toplvl.bind("<KeyPress-Right>"   ,self.a_right) #
        toplvl.bind("<KeyRelease-Right>" ,self.d_right) #
                                                        #
        self.leftbtn  = False                           #
        self.rightbtn = False                           #
        #                :: Shoot ::                    #
        toplvl.bind("<KeyPress-space>"  , self.a_shot)  #
        toplvl.bind("<KeyRelease-space>", self.d_shot)  #
                                                        #
        self.shotbtn  = False                           #
        self.cooldown = True                            #
        #===============================================#

        self.Starbirth()
        self.StarshipBirth()

        #Game Starts#
        "==========="
        self.Update()
        "==========="
        #Game Starts#
        
    """
    Method self.Update is always running
    """
    "==============="
    def Update(self):
        self.SpaceShift()
        self.LaserBeams()
        self.AsteroidRain()
        self.moveMF()
        self.shootMF()
        self.timeboard['text'] = 'time: %.3f' % (process_time()-self.start)
        self.root.after(self.LAPSO , self.Update)
    "==============="

    def get_score(self):
        return int(ceil((process_time()-self.start)*self.score))

    def get_name(self, event):
        name = self.p_name.get()
        pts  = self.get_score()
        self.menu.ranking.update(name, pts)
        self.menu.ranking.save()
        self.askforname.place_forget()
        self.root.destroy()
        main()

    """
    self.GameOver finishes game.
    """
    "================="
    def GameOver(self):
        self.quit = True
        self.LAPSO = 999999999
        self.contador = 0
        self.gameoverlabel = Label(self.Space,font=("arial black",80,"bold"),
                                   text = "GAME OVER", fg = "yellow", bg = "black")
        self.gameoverlabel.place(relx=0.2, rely=0.002)

        ranks = map(lambda x: x[1], self.menu.ranking.list)
        
        if ranks == []:
            self.play_gif(self.WIN_seq)
            
        elif self.get_score() >= max(ranks): 
            self.play_gif(self.WIN_seq)
        else:
            self.play_gif(self.LOST_seq)
        self.askforname.place(relx=0.5, rely=0.5)
        self.answer.focus()
        self.root.bind("<Return>", self.get_name)
    
    "================="

    """
    Show animation
    """
    "======================"
    def play_gif(self, seq):
        if self.contador <= len(seq):
            frame = seq[self.contador]
            self.actual_frame = self.Space.create_image(w/2,int(h/1.7) ,image=frame)
            self.contador += 1
            self.root.after(100, self.play_gif, seq)
        else:
            return
    "======================"
    
    """
    Control starship movement and shooting
    """
    "======================"
    def a_shot(self, event):
        self.shotbtn  = True
        
    def d_shot(self, event):
        self.shotbtn  = False
        self.cooldown = True
    
    def a_left(self, event):
        self.leftbtn = True
    def d_left(self, event):
        self.leftbtn = False

    def a_right(self, event):
        self.rightbtn = True
    def d_right(self, event):
        self.rightbtn = False
    "======================"
    
    """
    Millenium Falcon is always checking for movement
    """
    "================"
    def moveMF(self):
        X,Y = self.Space.coords(self.MF)

        VEL = 10
        
        L_INSIDE = X >= self.MF_WIDTH
        R_INSIDE = X <= self.LX - self.MF_WIDTH
        
        if self.rightbtn and R_INSIDE:
            self.Space.move(self.MF,+VEL,0) 
        if self.leftbtn and L_INSIDE:
            self.Space.move(self.MF,-VEL,0)
    "================"

    """
    Shooting is done with the spacebar
    """
    "======================="
    def shootMF(self):
        if self.shotbtn and self.cooldown:
            X,Y = self.Space.coords(self.MF)
##            self.root.after(10,play_sound, "blaster.wav")
            #print (thread._count())
            self.tirosrebeldes.append(self.Space.create_image(X,Y-60,
                                                              image=self.LASER_img))
            self.cooldown = False
    "======================="    

    def fire_fighter(self, fighter):
##        self.root.after(10,play_sound, "tie_blaster.wav")
        #print (thread._count())
        self.tirosdoImperio.append(self.Space.create_image(
                                   self.Space.coords(fighter)[0],
                                   self.Space.coords(fighter)[1]+30,
                                   image=self.LASER_img))
                                   
    def checkCollisionFighterMF(self):
        a,b = self.Space.coords(self.MF)[0],self.Space.coords(self.MF)[1]
        for fighter in self.Fighters:
            x,y = self.Space.coords(fighter)[0],self.Space.coords(fighter)[1]
            if ((a-x)**2+(b-y)**2)**0.5<40:
                self.Kaboom(fighter)
                self.Space.create_image(self.Space.coords(self.MF)[0],
                                        self.Space.coords(self.MF)[1],
                                        image=self.Explosion[4])
                self.GameOver()
            
    def checkIfLaserHitMF(self,laser,MF):
        try:
            verificacao=[abs(self.Space.coords(laser)[0]-self.Space.coords(MF)[0])<29,
                         self.Space.coords(MF)[1]-self.Space.coords(laser)[1]<20,
                         self.Space.coords(laser)[1]-self.Space.coords(MF)[1]<20]
        except:
            verificacao=[False,False,False]
            
        if all(verificacao):
            self.Space.create_image(self.Space.coords(MF)[0],
                                    self.Space.coords(MF)[1],
                                    image=self.Explosion[4])
            self.Space.delete(laser)
            self.tirosdoImperio.remove(laser)
            self.GameOver()

    def didLaserDestroyFighters(self,laser,lista):
        for fighter in lista:
            try:
                verificacao=[abs(self.Space.coords(laser)[0]-self.Space.coords(fighter)[0])<20,
                             self.Space.coords(laser)[1]-self.Space.coords(fighter)[1]<15,
                             self.Space.coords(fighter)[1]-self.Space.coords(laser)[1]<15]
            except:
                verificacao=[False,False,False]
                
            if all(verificacao):
                self.Kaboom(fighter, laser)
                
    def Kaboom(self, AsInimigx, laser=None):
        contador=0
        explosion=[]
        def explodindo(coordsdAsInimigx,coordslaser,contador,explosion,check=True):
            if contador>1:
                for gifAntigo in explosion:
                    self.Space.delete(gifAntigo)
                    explosion.remove(gifAntigo)
            
            if contador==0:
                self.Space.delete(AsInimigx)      
                self.Fighters.remove(AsInimigx)
            
            if contador<7: 
                explosion.append(self.Space.create_image(
                             coordslaser[0],coordsdAsInimigx[1],
                             image=self.Explosion[contador]))
                contador+=1
                self.root.after(120,explodindo,coordsdAsInimigx,coordslaser,contador,explosion)           
            if contador==7:
                self.Space.delete(explosion[0])
        
        if laser!=None:
##            thread.start_new_thread(play_sound, ("explosion.wav",))
            explodindo(self.Space.coords(AsInimigx),self.Space.coords(laser),contador,explosion)
            self.Space.delete(laser)      
            self.tirosrebeldes.remove(laser)
            self.score += 1
            self.scoreboard['text'] = 'fighters: %d'%self.score
            self.levelincrease()
        if laser==None:
            explodindo(self.Space.coords(AsInimigx),self.Space.coords(AsInimigx),contador,explosion,False)
        
    def createAsteroid(self,x,y,asteroid='random'):
        vetor = (3*cos(pi*random()), 4 + 6*random())
        if asteroid == 'random':
            self.AsteroidsPlaced+=[((self.Space.create_image(x,y,image=choice(self.Asteroids))), vetor)]
        else:
            self.AsteroidsPlaced+=[self.Space.create_image(x,y,image=asteroid), vetor]
            
    def checkForAsteroidsCollisions(self, asteroide):
        a,b = self.Space.coords(asteroide)[0],self.Space.coords(asteroide)[1]
        for fighter in self.Fighters:
            x,y = self.Space.coords(fighter)[0],self.Space.coords(fighter)[1]
            if ((a-x)**2+(b-y)**2)**0.5<55:
                self.Kaboom(fighter)
                
        x,y = self.Space.coords(self.MF)[0],self.Space.coords(self.MF)[1]
        if ((a-x)**2+(b-y)**2)**0.5<70:
            self.Space.create_image(self.Space.coords(self.MF)[0],
                                    self.Space.coords(self.MF)[1],
                                    image=self.Explosion[4])
            self.GameOver()
        
    def SpaceShift(self):
        dy = self.VEL
        for star in self.Stars:
            
            x1,y1,x2,y2 = self.Space.coords(star)
            
            x,y = (x1+x2)/2.0,(y1+y2)/2.0
            
            s = abs(x1-x2)/2.0
 
            if y - dy > self.LY:
                self.Space.coords(star, x+s,s,x-s,-s)

            self.Space.move(star, 0, dy)

    def levelincrease(self):
        if self.score%10*self.nivel == 0:
            self.nivel += 1

    def LaserBeams(self):
        for tiro in self.tirosrebeldes:
            """move rebel lasers up"""
            self.Space.move(tiro,0,-15)
            
            if self.Space.coords(tiro)[1]<0:
                self.Space.delete(tiro)      
                self.tirosrebeldes.remove(tiro)
                
            else:
                 self.didLaserDestroyFighters(tiro, self.Fighters)
            
        for tiro in self.tirosdoImperio:
            """move empire lasers down"""
            self.Space.move(tiro,0,15)
            if self.Space.coords(tiro)[1]>self.LY:
                self.Space.delete(tiro)            
                self.tirosdoImperio.remove(tiro)     
            self.checkIfLaserHitMF(tiro,self.MF)
         
    def AsteroidRain(self):
        for (asteroide,vetor) in self.AsteroidsPlaced:
            """Move asteroids"""
            self.Space.move(asteroide,vetor[0],vetor[1])
            self.checkForAsteroidsCollisions(asteroide)
            try:
                """Stop lasers that collide with asteroids"""
                a,b = self.Space.coords(asteroide)[0],self.Space.coords(asteroide)[1]
                for laser in self.tirosrebeldes:
                    x,y = self.Space.coords(laser)[0],self.Space.coords(laser)[1]
                    verificacao = ((a-x)**2+(b-y)**2)**0.5<30
                    if verificacao:
                        self.Space.delete(laser)
                        self.tirosrebeldes.remove(laser)
                    
                for laser in self.tirosdoImperio:
                    x,y = self.Space.coords(laser)
                    if ((a-x)**2+(b-y)**2)**0.5<30:
                        self.Space.delete(laser)
                        self.tirosdoImperio.remove(laser)
            except:
                pass
            
            if self.Space.coords(asteroide)[1]>self.LY:
                self.Space.delete(asteroide)            
                self.AsteroidsPlaced.remove((asteroide,vetor))
             
        self.checkCollisionFighterMF()

    def Starbirth(self):
        """
        Creates game stars
        """
        def get_color():
            KEY = random()
            if KEY < 0.92:
                return '#ffffff'
            elif KEY < 0.96:
                return '#ffff33'
            elif KEY < 0.99:
                return '#ff0022'
            else:
                return '#000055'
                   
        for star in range(int(self.stars)):
            
            x, y, r = self.LX*random(), self.LY*random(), 2*random()
            color = get_color()
            
            self.Stars.append(
                              self.Space.create_oval(x+r, y+r, x-r, y-r,
                                                     fill=color,outline=color)
                              )

    def StarshipBirth(self):
        """
        Create Game Ships
        """

        """
        --*-- Millenium Falcon --*--
        """

        MF_POSX = self.LX*0.50
        MF_POSY = self.LY*0.85

        self.MF_img = PhotoImage(master=self.root,file='./assets/Millenium Falcon 2.gif')
        self.MF = self.Space.create_image(MF_POSX, MF_POSY, image=self.MF_img)

        self.MF_WIDTH  = int(self.MF_img.width() /2) + 1
        self.MF_HEIGHT = int(self.MF_img.height()/2) + 1        

        """
        --*-- TIE Fighter --*--
        """
   
        self.FIGHTER_img = PhotoImage(master=self.root,file='./assets/Fighter3.gif')

        self.FIGHTER_WIDTH  = int(self.FIGHTER_img.width() /2) + 1 
        self.FIGHTER_HEIGHT = int(self.FIGHTER_img.height()/2) + 1 

        """
        --*-- Lasers --*--
        """

        self.LASER_img = PhotoImage(master=self.root,file='./assets/Laser Vermelho.gif')

        """
        --*-- Asteroids --*--
        """
        
        self.Asteroids = [PhotoImage(master=self.root,file='./assets/Asteroid%d.gif'%i) for i in range(1,3)]
        self.AsteroidsPlaced = []
        
        """
        --*-- Explosion Sequence --*--
        """
        
        self.Explosion = [PhotoImage(master=self.root,file='./assets/Explosion%d.gif'%i) for i in range(1,8)]


        """
        --*-- Videos --*--
        """
        self.LOST_seq = [PhotoImage(master=self.root,file="./assets/Scene%d.gif"%i) for i in range(1,16)]
        self.WIN_seq  = [PhotoImage(master=self.root,file="./assets/frame_%d_delay-0.1s.gif"%i) for i in range(28)]        

def main():
    menu = Menu()
    
#if  __name__ == '__main__':
main()