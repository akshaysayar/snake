
from cv2 import cv2
import random
from pynput import keyboard
from time import sleep
import multiprocessing
import sys,os
import time
import math
import pandas as pd
import numpy as np
# import tflearn
import math
# from tflearn.layers.core import input_data, fully_connected
# from tflearn.layers.estimator import regression
import pickle
def game(button,inputs):
 #variables
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1700)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1700)
    
   
    length = 15
    speed = 10
    choices = [i for i in range(50,600,10)]
    food_x = random.choice(choices)
    food_y = random.choice(choices)

    # rect_1_x = random.choice(choices)
    # rect_1_y = random.choice(choices)

    # rect_2_x = random.choice(choices)
    # rect_2_y = random.choice(choices)

    y_fence=[20,680]
    x_fence = [30,1240]

    xs = [80]*length
    ys = [80]*length
    previous_button = 0

    score = 0
    game_over = False
    #print(food_x,food_y)

    counter = 0
 #while loop
    while not game_over:

  #init and boundary and food
        img = cv2.flip(cap.read()[1],1)
        #draw boundary
        cv2.rectangle(img,(30,20), (1240,680), (230,150,44), 3)
        
        #draw food
        cv2.circle(img, (food_x,food_y), 15 , (255,0,155), -1)
        
  #movement of snake
        if button.value==3 and previous_button==1:
            button.value =previous_button
            #direction = previous_button
            previous_button = 0
        elif button.value == 4 and previous_button==2:
            button.value =previous_button
            #direction = previous_button
            previous_button = 0
        elif button.value == 2 and previous_button==4:
            button.value =previous_button
            #direction = previous_button
            previous_button = 0
        elif button.value == 1 and previous_button==3:
            button.value =previous_button
            #direction = previous_button
            previous_button = 0
        else:
            button.value = button.value
        
        if button.value==3 and previous_button!=1:
            previous_button = button.value
            temp = xs#[i-5 for i in xs]
            xs = []
            xs.append(temp[0]+speed)
            xs.extend(temp[0:-1])
            temp = ys
            ys = []
            ys.append(temp[0])
            ys.extend(temp[0:-1])
        elif button.value == 4 and previous_button!=2:
            previous_button = button.value
            temp = xs
            xs = []
            xs.append(temp[0])
            xs.extend(temp[0:-1])
            temp = ys#[i-5 for i in ys]
            ys = []
            ys.append(temp[0]+speed)
            ys.extend(temp[0:-1])
        elif button.value == 2 and previous_button!=4:
            previous_button = button.value
            temp = xs
            xs = []
            xs.append(temp[0])
            xs.extend(temp[0:-1])
            temp = ys#[i+5 for i in ys]
            ys = []
            ys.append(temp[0]-speed)
            ys.extend(temp[0:-1])
        elif button.value == 1 and previous_button!=3:
            previous_button = button.value
            temp = xs#[i+5 for i in xs]
            xs = []
            xs.append(temp[0]-speed)
            xs.extend(temp[0:-1])
            temp = ys
            ys = []
            ys.append(temp[0])
            ys.extend(temp[0:-1])
        
                #calculate angle
       
  #draw snake
        for i in range(length-1):
            cv2.line(img,(xs[i],ys[i]),(xs[i+1],ys[i+1]),(55,55,255),10)

 
            angle = (math.atan2(food_y-ys[0], food_x-xs[0]))
            angle = math.degrees((angle + (math.pi)/2) % (2*math.pi) - math.pi)*1
            angle = angle/180

         #if eat food
        
  #eating food
        if xs[0] in range(food_x-15,food_x+15) and ys[0] in range(food_y-15,food_y+15):
            xs.append(xs[-1])
            ys.append(ys[-1])
            length=length+1
            score = score +1

            food_x = random.choice(choices)
            food_y = random.choice(choices)
        
  #display score
        cv2.putText(img, str(score), (1, 40), cv2.FONT_HERSHEY_PLAIN, 2,(50,20,220), 3)

  #condition for game over
        l =[[xs[i],ys[i]] for i in range(length)]
        if 30>=xs[0] or xs[0]>=1240 or 20>=ys[0] or ys[0]>=680 or [xs[0],ys[0]] in l[1:]:
            game_over = True

        safety_distance = 10
 #calculate angles
        if button.value==1:
            angle = (math.atan2(ys[0]-food_y, xs[0]-food_x))
            angle = math.degrees((angle + math.pi) % (2*math.pi) - math.pi)
            angle = angle/180

            if [xs[0],ys[0]-safety_distance] in l or ys[0]-safety_distance in y_fence:
                right = 1
            else:
                right =0
            if [xs[0],ys[0]+safety_distance] in l or ys[0]+safety_distance in y_fence:
                left = 1
            else:
                left = 0
            if [xs[0]-safety_distance,ys[0]] in l or xs[0]-safety_distance in x_fence:
                front = 1
            else:
                front = 0

        if button.value==3:
            angle = (math.atan2(food_y-ys[0], food_x-xs[0]))
            angle = math.degrees((angle + math.pi) % (2*math.pi) - math.pi)
            angle = angle/180

            if [xs[0],ys[0]+safety_distance] in l or ys[0]+safety_distance in y_fence:
                right = 1
            else:
                right =0
            if [xs[0],ys[0]-safety_distance] in l or ys[0]-safety_distance in y_fence:
                left = 1
            else:
                left = 0
            if [xs[0]+safety_distance,ys[0]] in l or xs[0]+safety_distance in x_fence:
                front = 1
            else:
                front = 0

        if button.value==2:
            angle = (math.atan2(ys[0]-food_y, xs[0]-food_x))
            angle = math.degrees((angle + (math.pi)/2) % (2*math.pi) - math.pi)
            angle = angle/180

            if [xs[0]+safety_distance,ys[0]] in l or xs[0]+safety_distance in x_fence:
                right = 1
            else:
                right =0
            if [xs[0]-safety_distance,ys[0]] in l or xs[0]-safety_distance in x_fence:
                left = 1
            else:
                left = 0
            if [xs[0],ys[0]-safety_distance] in l or ys[0]-safety_distance in y_fence:
                front = 1
            else:
                front = 0

        if button.value==4:
            angle = (math.atan2(food_y-ys[0], food_x-xs[0]))
            angle = math.degrees((angle + (math.pi)/2) % (2*math.pi) - math.pi)*1
            angle = angle/180

            if [xs[0]-safety_distance,ys[0]] in l or xs[0]-safety_distance in x_fence:
                right = 1
            else:
                right =0
            if [xs[0]+safety_distance,ys[0]] in l or xs[0]+safety_distance in x_fence:
                left = 1
            else:
                left = 0
            if [xs[0],ys[0]+safety_distance] in l or ys[0]+safety_distance in y_fence:
                front = 1
            else:
                front = 0

  #maintain length of list = 6
        if len(inputs)>5:
            inputs.pop()
      
  #calculate distance
        dist = math.sqrt(((xs[0]-food_x)*(xs[0]-food_x))+((ys[0]-food_y)*(ys[0]-food_y)))

  #create list of inputs
        inputs.append([counter,round(dist,2),round(angle,3),left,front,right,button.value])
        #print(l)
        
  #reamining code
        counter =counter+ 1


        cv2.imshow("Snake", img)
        cv2.waitKey(1)


        #----------------------------------------------------------------------------------------------
 #outside while loop finishing window
    img = cv2.flip(cap.read()[1],1)
    cv2.putText(img, str("Game over"), (250, 200), cv2.FONT_HERSHEY_PLAIN, 10,(50,20,220), 20)
    cv2.putText(img, "score is "+str(score), (230, 600), cv2.FONT_HERSHEY_PLAIN, 10,(50,20,220), 20)
    cv2.imshow("Snake", img)
    button.value=17
    #cv2.waitKey(100000)

def controller(button):
    exit_flag = False
    global ct
    ct=0


    def on_press(key):
        try:
            print('alphanumeric key {0} pressed'.format(key.char))
        except AttributeError:
            print('special key {0} pressed'.format(key))
            
                

    def on_release(key):
        print('{0} released'.format(key))
        
        if key == keyboard.Key.left:
            button.value =1
        elif key == keyboard.Key.up:
            button.value =2
        elif key == keyboard.Key.right:
            button.value =3
        elif key == keyboard.Key.down:
            button.value =4
        

    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        
        print("listen...")
        
        while not exit_flag:
            pass
        
        listener.join()

def ai(button,inputs):
    pass
    # previous =-1
    # network = input_data(shape=[None, 5, 1], name='input')
    # network = fully_connected(network, 1, activation='linear')
    # network = regression(network, optimizer='adam', learning_rate=1e-2, loss='mean_square', name='target')
    # model = tflearn.DNN(network, tensorboard_dir='log')
    # model.load("/home/akshay/data/personal/Python_projects/Snake/model/version_1.tflearn")
    # print("-------------")
    # while True:
    #     if button.value!=17 and len(inputs)!=0 and previous!=inputs[-1][0]:
    #         print(len(inputs),inputs[-1])
    #         previous = inputs[-1][0]
    #         # training_data.append(inputs[-1])
    #         # print("88888888888888888888888888888888888888888888888888")
            
    #         # prediction = model.predict(inputs[-1][1:-1].reshape(-1, len(inputs[1:-1]), 1))
    #         # action = np.argmax(prediction[0])
    #         #print(action)
    #         #button.value=action

def printing(button,inputs,path):
    training_data = []
    cols =[ '3', '4', '5', '6']
    d_map = {'40':4, '41':3 , '42':1, '10':1, '11':4, '12':2, '20':2, '21':1,'22':3, '30':3,'31':2, '32':4}
    #LReg = LReg= pickle.load(open("/home/akshay/data/personal/Python_projects/Snake/model/LR_v1.pkl", 'rb'))
    previous =-1
    previous2= 3
    previous_dir = 3
    action = 3
    while True:
        if button.value!=17 and len(inputs)!=0 and previous2!=inputs[-1][0]:
            training_data.append(inputs[-1][2:-1])
            #print(len(inputs),)
            # l =[]
            # l.append(inputs[-1][2:-1])
            # df = pd.DataFrame(l,columns=cols)
            # symbol = LReg.predict(df)
            # prob = LReg.predict_proba(df)
            # pr = prob[0,prob.argmax(1).item()]inputs[-1][2:-1]
            # print(symbol,prob,pr)

            # ar=np.array(inputs[-1][2:-1]).reshape(-1, 4, 1)
            # print(ar)
            # prediction = model.predict(ar)
            # action = np.argmax(prediction[0])
            # print("prediction",prediction)
            # print("action",action)

            # direct = d_map(str(previous_dir)+str(action))
            # print(direct)

            if inputs[-1][3]==0 and inputs[-1][5]==0 and inputs[-1][4]==0:
                if inputs[-1][2]<0 :
                    action = d_map[str(previous_dir)+str(1)]
                    training_data[-1].append(1)
                elif inputs[-1][2]>0:
                    action = d_map[str(previous_dir)+str(2)]
                    training_data[-1].append(2)
                elif inputs[-1][2]==0 :
                    action = d_map[str(previous_dir)+str(0)]
                    training_data[-1].append(0)
            
            elif inputs[-1][3]==1 and inputs[-1][5]==0 and inputs[-1][4]==0:
                # if inputs[-1][2]<0 :
                #     action = d_map[str(previous_dir)+str(1)]
                #     training_data[-1].append(1)
                if inputs[-1][2]>0:
                    action = d_map[str(previous_dir)+str(2)]
                    training_data[-1].append(2)
                elif inputs[-1][2]==0 :
                    action = d_map[str(previous_dir)+str(0)]
                    training_data[-1].append(0)
                else:
                    action = d_map[str(previous_dir)+str(0)]
                    training_data[-1].append(0)
            
            elif inputs[-1][3]==0 and inputs[-1][5]==1 and inputs[-1][4]==0:
                if inputs[-1][2]<0 :
                    action = d_map[str(previous_dir)+str(1)]
                    training_data[-1].append(1)
                # if inputs[-1][2]>0:
                #     action = d_map[str(previous_dir)+str(2)]
                #     training_data[-1].append(2)
                elif inputs[-1][2]==0 :
                    action = d_map[str(previous_dir)+str(0)]
                    training_data[-1].append(0)
                else:
                    action = d_map[str(previous_dir)+str(0)]
                    training_data[-1].append(0)

            elif inputs[-1][3]==0 and inputs[-1][5]==0 and inputs[-1][4]==1:
                if inputs[-1][2]<0 :
                    action = d_map[str(previous_dir)+str(1)]
                    training_data[-1].append(1)
                elif inputs[-1][2]>0:
                    action = d_map[str(previous_dir)+str(2)]
                    training_data[-1].append(2)
                # elif inputs[-1][2]==0 :
                #     action = d_map[str(previous_dir)+str(0)]
                #     training_data[-1].append(0)
                else:
                    action = d_map[str(previous_dir)+str(1)]
                    training_data[-1].append(1)


            elif inputs[-1][3]==1 and inputs[-1][5]==1 and inputs[-1][4]==0:
                action = d_map[str(previous_dir)+str(0)]
                training_data[-1].append(0)

            elif inputs[-1][3]==1 and inputs[-1][5]==0 and inputs[-1][4]==1:
                action = d_map[str(previous_dir)+str(2)]
                training_data[-1].append(2)

            elif inputs[-1][3]==0 and inputs[-1][5]==1 and inputs[-1][4]==1:
                action = d_map[str(previous_dir)+str(1)]
                training_data[-1].append(1)

            else:
                print("DOOOOoOOooOOOooooooooOOOOooommmedddddd")
                action = d_map[str(previous_dir)+str(0)]
                training_data[-1].append(0)

            if inputs[-1][2]<0 and inputs[-1][3]==0:
                action = d_map[str(previous_dir)+str(1)]
                training_data[-1].append(1)
            elif inputs[-1][2]>0 and inputs[-1][5]==0:
               action = d_map[str(previous_dir)+str(2)]
               training_data[-1].append(2)
            elif inputs[-1][2]==0 and inputs[-1][4]==0:
                action = d_map[str(previous_dir)+str(0)]
                training_data[-1].append(0)
            else:
                training_data[-1].append(0)

            print(training_data[-1])
            #print('aaction---',action)
            previous2 = previous
            previous = inputs[-1][0]
            previous_dir = button.value
            button.value = action
            #button_value = symbol
            #button_value = direct
            #button.value=int(prediction)
            #training_data.append(inputs[-1])
        elif button.value==17:
            break
    pd.DataFrame(training_data).to_csv(path,index=False)

def main(i):
    path = "/home/akshay/data/personal/Python_projects/Snake/data/training_data_"+str(i)+".csv"
    flag_1 = multiprocessing.Value('i',3)
    flag_2 = multiprocessing.Value('i',False)
    manager = multiprocessing.Manager()
    inputs = manager.list()

    p1 = multiprocessing.Process(target=game, args=(flag_1,inputs))

    #p2 = multiprocessing.Process(target=ai, args=(flag_1,inputs))
    p3 = multiprocessing.Process(target=printing, args=(flag_1,inputs,path))
    p1.start()
    print("starting process 2")
    #time.sleep(10)
    #p2.start()
    p3.start()
    p1.join()
    #p2.join()

if __name__ == "__main__":
    for i in range(9,101):
        main(i)