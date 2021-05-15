from cv2 import cv2
import random
from pynput import keyboard
from time import sleep
import pandas as pd
import numpy as np
import pickle

class Snake():

    def __init__(self):

        self.LReg = pickle.load(open("/home/akshay/data/personal/Python_projects/Snake/model/RF_v2.pkl", 'rb'))

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1700)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1700)

        self.length = 12
        self.speed = 10
        
        self.y_fence=[20,680]
        self.x_fence = [30,1240]

        self.xs = [80]*self.length
        self.ys = [80]*self.length
        self.snak = [(self.xs[i],self.ys[i]) for i in range( self.length)]
        self.previous_button = 0

        self.choices_x = [i for i in range(40,1230,10)]
        self.choices_y = [i for i in range(30,670,10)]
        self.direction = "right"
        self.score = 0
        self.game_over = False
        self.state_l_f_r_fl_fu_fr_fd = [0,0,0,0,0,0,0]
        self.counter = 0

        self.colors = {"maroon":(0,0,128),"brown":(42,42,165),"red":(0,0,255),"dark_green":(0,100,0),"grey":(47,49,49),"yellow":(0,215,255)}
        self.set_food()

    def set_food(self):
        self.food_x = random.choice(self.choices_x)
        self.food_y = random.choice(self.choices_y)

    def game(self):
        while not self.game_over:
            img = cv2.flip(self.cap.read()[1],1)
            cv2.rectangle(img,(self.x_fence[0],self.y_fence[0]), (self.x_fence[1],self.y_fence[1]), self.colors["dark_green"], 3)
            
            cv2.circle(img, (self.food_x,self.food_y), 15 , self.colors["maroon"], -1)

            
            self.state_l_f_r_fl_fu_fr_fd = self.states()
            print(self.state_l_f_r_fl_fu_fr_fd)
            # self.key(self.direction)
            # self.automated()
            self.ml()
            
            self.move()
            self.food_eat()
            self.end_game()

            for i in range(self.length-1):
                cv2.line(img,self.snak[i],self.snak[i+1],self.colors['yellow'],10)

            cv2.putText(img, str(self.score), (1, 40), cv2.FONT_HERSHEY_PLAIN, 2,self.colors["red"], 3)
            cv2.imshow("Snake", img)            
            cv2.waitKey(1)

    def move(self):
        if self.direction == "right":
            self.snak[1:]=self.snak[:-1]
            self.snak[0]=(self.snak[0][0]+self.speed,self.snak[0][1])
        elif self.direction == "left":
            self.snak[1:]=self.snak[:-1]
            self.snak[0]=(self.snak[0][0]-self.speed,self.snak[0][1])
        elif self.direction == "down":
            self.snak[1:]=self.snak[:-1]
            self.snak[0]=(self.snak[0][0],self.snak[0][1]+self.speed)
        elif self.direction == "up":
            self.snak[1:]=self.snak[:-1]
            self.snak[0]=(self.snak[0][0],self.snak[0][1]-self.speed)

    def end_game(self):
        if self.snak[0] in self.snak[1:] or self.snak[0][0] in self.x_fence or self.snak[0][1] in self.y_fence:
            self.game_over = True 

    def food_eat(self):
        if (self.food_x,self.food_y) == self.snak[1]:
            self.set_food()
            self.snak.append(self.snak[-1])
            self.score +=1
            self.length +=1

    def states(self):
        direction = self.direction
        x,y = self.snak[0][0],self.snak[0][1]
        speed = self.speed
        fx,fy = self.food_x-x,self.food_y-y
        
        l,f,r=0,0,0
        fl,fu,fr,fd=0,0,0,0

        if direction=="left":
            if (x,y+speed) in self.snak[1:] or y+speed in self.y_fence:
                l=1
            if (x-speed,y) in self.snak[1:] or x-speed in self.x_fence:
                f=1
            if (x,y-speed) in self.snak[1:] or y-speed in self.y_fence:
                r=1

            if fx<0: fu,fd=1,0
            elif fx>0:  fu,fd=0,1
            else: fu,fd=0,0

            if fy<0: fr,fl= 1,0
            elif fy>0: fr,fl= 0,1
            else: fr,fl= 0,0

        elif direction=="up":
            if (x-speed,y) in self.snak[1:] or x-speed in self.x_fence:
                l=1
            if (x,y-speed) in self.snak[1:] or y-speed in self.y_fence:
                f=1
            if (x+speed,y) in self.snak[1:] or x+speed in self.x_fence:
                r=1

            if fy<0: fu,fd=1,0
            elif fy>0:  fu,fd=0,1
            else: fu,fd=0,0

            if fx<0: fr,fl= 0,1
            elif fx>0: fr,fl= 1,0
            else: fr,fl= 0,0
            

        elif direction=="right":
            if (x,y-speed) in self.snak[1:] or y-speed in self.y_fence:
                l=1
            if (x+speed,y) in self.snak[1:] or x+speed in self.x_fence:
                f=1
            if (x,y+speed) in self.snak[1:] or y+speed in self.y_fence:
                r=1

            if fx<0: fu,fd=0,1
            elif fx>0:  fu,fd=1,0
            else: fu,fd=0,0

            if fy<0: fr,fl= 0,1
            elif fy>0: fr,fl= 1,0
            else: fr,fl= 0,0

        elif direction=="down":
            if (x+speed,y) in self.snak[1:] or x+speed in self.x_fence:
                l=1
            if (x,y+speed) in self.snak[1:] or y+speed in self.y_fence:
                f=1
            if (x-speed,y) in self.snak[1:] or x-speed in self.x_fence:
                r=1

            if fy<0: fu,fd=0,1
            elif fy>0:  fu,fd=1,0
            else: fu,fd=0,0

            if fx<0: fr,fl= 1,0
            elif fx>0: fr,fl= 0,1
            else: fr,fl= 0,0

        return([l,f,r,fl,fu,fr,fd])
        

    
        pass

    def key(self,direct):
        dir = ["left","up","right","down"]
        new = random.choice(dir)
        if dir[(dir.index(direct)+2)%4]==new:
            self.direction = direct
        else:
            self.direction = new

    def automated(self):
        dir = ["left","up","right","down"]
        previous = self.direction
        state = self.state_l_f_r_fl_fu_fr_fd
        l,f,r,fl,fu,fr,fd = state[0],state[1],state[2],state[3],state[4],state[5],state[6]
        #d_map = {'l':0,'f':1,'r':2}
        d = None
        if l==0 and f==0 and r==0:
            if fu==1: d = 'f'
            elif fl==1: d = 'l'
            elif fr==1: d = 'r'
            else: d = random.choice(['l','r'])
        elif l==1 and f==0 and r==0:
            if fu==1: d='f'
            else: d = 'r'
        elif l==0 and f==0 and r==1:
            if fu==1: d='f'
            else: d = 'l'
        elif l==0 and f==1 and r==0:
            if fl==1: d='l'
            else: d = 'r'
        elif l==1 and f==0 and r==1:
            d= 'f'
        elif l==0 and f==1 and r==1:
            d = 'l'
        elif l==1 and f==1 and r==0:
            d='r'

        
        if d=='f':
            direction =  previous
        elif d=='l':
            direction = dir[(dir.index(previous)+3)%4]
        elif d=='r':
            direction = dir[(dir.index(previous)+1)%4]

        self.direction = direction

    def ml(self):
        previous = self.direction
        dir = ["left","up","right","down"]
        state = self.state_l_f_r_fl_fu_fr_fd
        cols =[ '1','2','3','left', 'front', 'right', 'down']
        l=[]
        l.append(state)
        df = pd.DataFrame(l,columns=cols)
        symbol = self.LReg.predict(df)
        
        if symbol[0]==0:
            direction =  previous
        elif symbol[0]==1:
            direction = dir[(dir.index(previous)+3)%4]
        elif symbol[0]==2:
            direction = dir[(dir.index(previous)+1)%4]
        self.direction = direction

def main():
    snake = Snake()
    snake.game()
    
if __name__ == "__main__":
    main()
