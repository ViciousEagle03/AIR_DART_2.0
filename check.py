import mediapipe as mp
import cv2
import math
import time
import numpy as np
from Score_board import Scoreboard
from dart import Dart
from constants import MY_RESOLUTION__X,MY_RESOLUTION__Y,DART_SIZE,CAM_RES
import os
import cvzone
#cvzone to overlay image
DART_POS = (500,500)
DART_HIT = False
CAPTURED = False
FIRST_ITERATION = False
DART_FALLING = False
DART_RESIZE=[100,100]
RM = False
pos_fall=(0,0)
resize=1
p=False
k=0
allowgrab=True
score=0
#OBJ creation for different class
power = 0.0
distance_hand_from_s = 0.0
scoreboard = Scoreboard()


#Creating linear regression function for x(distance between 5 and 17) and y(distance in cm) to track the distance of hand from screen
DIST_5AND17 = [300,245,200,170,145,130,112,103,93,87,80,75,70,67,62,59,57]
DIST_FROM_SCREEN_IN_CM = [20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
COEFF = np.polyfit(DIST_5AND17,DIST_FROM_SCREEN_IN_CM,2)
A,B,C = COEFF

#Creating linear regression function for dfsh and power
DIST_8AND31 = [590,500,452,415,390,346,318,285,265,248,222,205,180,169,150,136,121]
COEFF1 = np.polyfit(DIST_8AND31,DIST_FROM_SCREEN_IN_CM,2)
A1,B1,C1 = COEFF1

DISTANCE8AND4 = [530,475,430,391,360.336,318,298,271,250,230,209,200,185,175,146,130,100]
COEFF2 = np.polyfit(DISTANCE8AND4 , DIST_FROM_SCREEN_IN_CM,2)
A2,B2,C2 = COEFF2

def distance_from_screen(coord_1 , coord_2):
    x1,y1  = coord_1
    x2,y2  = coord_2
    distance  = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    distanceCM = A*distance**2 + B*distance + C
    #print(f'distance{distance}')
    return distanceCM

def power_of_throw(coord_1,coord_2):
    x1,y1  = coord_1
    x2,y2  = coord_2
    distance  = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    pow_throw = A1*distance**2 + B1*distance + C1
    #print(f'distance{distance}')
    return pow_throw

def distance_8and4(coord_1,coord_2):
    x1,y1  = coord_1
    x2,y2  = coord_2
    distance  = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    distance8and4 = A2*distance**2 + B2*distance + C2
    return distance8and4

'''def hola(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global A,B,distance_hand_from_s,power
        A.append(distance_hand_from_s)
        B.append(power)
        print("skajyhdfgasljdyfgasjdfg")
    pass
'''
'''def animate(image,pointer_dart):
    global resize,DART_RESIZE,DART_SIZE,DART_POS
    dart_animate_01 = cv2.imread("dart_animate/Dart_1-rbg.png",cv2.IMREAD_UNCHANGED)
    dart_animate_1 = cv2.resize(dart_animate_01 , DART_SIZE)
    dart_animate_02 = cv2.imread("dart_animate/Dart_2-rbg.png",cv2.IMREAD_UNCHANGED)
    dart_animate_2 = cv2.resize(dart_animate_02 , DART_SIZE)
    dart_animate_03 = cv2.imread("dart_animate/Dart_3-rbg.png",cv2.IMREAD_UNCHANGED)
    dart_animate_3 = cv2.resize(dart_animate_03 , DART_SIZE)
    dart_animate_03 = cv2.imread("dart_animate/Dart_3-rbg.png",cv2.IMREAD_UNCHANGED)
    dart_animate_list = (dart_animate_1,dart_animate_2,dart_animate_3)
    DART_RESIZE = int(DART_SIZE[0] * resize),int(DART_SIZE[1]*resize)
    DART_POS1 = (DART_POS[0] - DART_RESIZE[0]//2 , DART_POS[1] - DART_RESIZE[1] //2 )
    
    
    dart_animate_4 = cv2.resize(dart_animate_list[pointer_dart] , DART_RESIZE)

    image = cvzone.overlayPNG(image,dart_animate_4,DART_POS1)
    print(f'size{DART_SIZE}')
    print(f'resize{DART_RESIZE}')
    print(f'pos{DART_POS}')
    resize = resize - 0.05
    return(image)'''
    

    
    
    

#uuid is the uniform unique identifier and it helps to
#prevent any overlap of images with the actual video feed

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


#mp.solutions is a module that provides a set of pre-built solutions
#for various computer vision and machine learning tasks. 
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,CAM_RES[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,CAM_RES[1])
cv2.namedWindow("AIRD",cv2.WND_PROP_FULLSCREEN)
#dart position set
#dart_demo = cv2.imread("dart_png.png",cv2.IMREAD_UNCHANGED)
#dart_demo1 = cv2.resize(dart_demo , DART_SIZE)

dart = Dart()

    
#cv2.setMouseCallback('AIRD',hola)

#
cv2.setWindowProperty('AIRD', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

start_time = time.time()
prev_distance_from_s=0

with mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence = 0.5) as hands:
    while cap.isOpened():
        
        window_name="AIRD"
        ret,frame = cap.read()
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
        
        image.flags.writeable =False
        results = hands.process(image)
        image.flags.writeable =True
        #print(results)
        image = cv2.cvtColor(image , cv2.COLOR_RGB2BGR)
        #image = cvzone.overlayPNG(image,dart_demo1,DART_POS)
        
        image_dart,dart_number=dart.dart_display(image)
        if dart_number>0:
            image = image_dart
        dart.allow_grab(allowgrab)
        image = dart.dart_board(image)

        
        #results.multi_hand_landmarks gives us all the 21 hand knuckle coordinates
       #print(results.multi_hand_landmarks)
        #Now we have the landmarks and we need to draw each of the handknuckle landmarks
        if results.multi_hand_landmarks:
            for num,finger in enumerate(results.multi_hand_landmarks):
               '''mp_drawing.draw_landmarks(image , finger , mp_hands.HAND_CONNECTIONS)
                ''' # the color of the line connecting the knuckles and the dots 
                # repressenting the knuckle can be changed by DrawingSpec method.
            #Calculating the distance from the index finger tip to a reference 
            # point here we take the reference ponjt to be(0,0)
            
            index_finger_tip = finger.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            reference_point = (0,0)
            thumb_finger_tip = finger.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_mcp = finger.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            pinky_mcp = finger.landmark[mp_hands.HandLandmark.PINKY_MCP]
            wrist = finger.landmark[mp_hands.HandLandmark.WRIST]
            #distance = math.dist(((index_finger_tip.x),(index_finger_tip.y)),reference_point)
            #distance = distance1 *255
            #print(distance)
            dimensions_window = cv2.getWindowImageRect(window_name)
            distance = math.dist(((index_finger_tip.x)*CAM_RES[0],(index_finger_tip.y)*CAM_RES[1]),((thumb_finger_tip.x)*CAM_RES[0],(thumb_finger_tip.y)*CAM_RES[1]))
            coord_x,coord_y= ((index_finger_tip.x + thumb_finger_tip.x) / 2) , ((index_finger_tip.y + thumb_finger_tip.y)/2)
            coord_x,coord_y = coord_x * CAM_RES[0],coord_y *CAM_RES[1]
            coord = (int(coord_x),int(coord_y))
            index_finger_coord = ((int(index_finger_tip.x *CAM_RES[0])) ,
                                  (int(index_finger_tip.y *CAM_RES[1])))
            index_finger_mcp_coord = ((int(index_finger_mcp.x *CAM_RES[0])) ,
                                  (int(index_finger_mcp.y *CAM_RES[1])))
            pinky_finger_mcp_coord = ((int(pinky_mcp.x *CAM_RES[0])) ,
                                  (int(pinky_mcp.y *CAM_RES[1])))
            wrist_coord = ((int(wrist.x)*CAM_RES[1]),
                     (int(wrist.y)*CAM_RES[0]))
            thumb_coord = (int(thumb_finger_tip.x)*CAM_RES[0],
                           int(thumb_finger_tip.y)*CAM_RES[1])
            power = math.dist(((wrist.x)*CAM_RES[0],(wrist.y)*CAM_RES[1]) , ((index_finger_tip.x)*CAM_RES[0],(index_finger_tip.y)*CAM_RES[1]))
    
            #print(coord_x)
            #print(coord_y)
            distance_hand_from_s= distance_from_screen(index_finger_mcp_coord,pinky_finger_mcp_coord)
            power_throw = power_of_throw(index_finger_coord,wrist_coord)
            power_throw = power_throw*2
            distance_throw = distance_8and4(index_finger_coord,thumb_coord)
            #print(distance_hand_from_s)
            ###################Check for throwing of dart
            INTERVAL =0.2
            current_time = time.time()
            #print(f'current_time{current_time}')
            #print(f'start{start_time}')
            if current_time - start_time >=INTERVAL :
                threw_dart =prev_distance_from_s - distance_hand_from_s
                if threw_dart >30 and  FIRST_ITERATION and CAPTURED:
                    cv2.putText(image ,f'{distance})',DART_POS,
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                    k=1
                    resize=1
                    pointer_dart=0

                prev_distance_from_s = distance_hand_from_s
                start_time=current_time
            
                
            FIRST_ITERATION =True
            #print(f'prev{prev_distance_from_s}')
            #print(f'new{distance_hand_from_s}')
          
            ###################
            '''if distance<70:
                if  DART_POS[0]< coord[0]<DART_POS[0]+ DART_SIZE[0] and DART_POS[1]<coord[1]<DART_POS[1]+DART_SIZE[1] or CAPTURED:
                    CAPTURED = True
                    new_pos =(coord[0] - DART_SIZE[0] //2, coord[1] - DART_SIZE[1]//2)
                    image = cvzone.overlayPNG(frame,dart_demo1,new_pos)
                    DART_POS =new_pos
            '''
            
            
            if distance<30 :
                DART_FALLING = False
                if dart.check_movement(coord) or CAPTURED:
                    CAPTURED =True
                    image,DART_POS = dart.moved(image,coord)
            elif(distance >=100):
                
                if CAPTURED:
                    dart.grav2(distance,threw_dart,power)
                    RM = True
                if not CAPTURED and not k==1 and dart.CAPTURED:
                    dart.dart_removed(image)
                    p=True
                    DART_FALLING = True
                    pointer_dart_falling =0
                    pos_fall = coord
                CAPTURED=False
                
            elif(distance>50 and distance<100 and not CAPTURED and threw_dart<20):
                if not CAPTURED and not k==1 and dart.CAPTURED:
                    dart.dart_removed(image)
                    p=True
                    DART_FALLING = True
                    pointer_dart_falling =0
                    pos_fall = coord
                CAPTURED=False
            
            #image = dart.wind_animate(image)
            '''elif(distance>30 and distance<130 and not CAPTURED and threw_dart<30):
                RM = True
                CAPTURED=False
                if not CAPTURED and not k==1 and dart.CAPTURED:
                    dart.dart_removed(image)
                print("trash..................................")'''
            cv2.putText(image ,f'power : {power}',(40,40),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.putText(image,f'distance{distance}',(40,60),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.putText(image,f'power/{int(power)}',(40,80),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.putText(image,f'disth_from_s/{int(distance_hand_from_s)}',(40,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.putText(image,f'index/{index_finger_coord}',(40,120),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            
        '''if k==1 and resize>=0.02:
            if pointer_dart ==3:
                pointer_dart=0
            image = animate(image,pointer_dart)
            allowgrab = False
            pointer_dart+=1
            if resize <=0.1:
                DART_HIT=True
                k=0
                allowgrab = True'''
        if k==1 and not CAPTURED:
            image,DART_HIT,allowgrab,pointer_dart,k = dart.resizing(pointer_dart,
                                                                    image,DART_HIT)
        image = scoreboard.display_scoreboard(image,DART_HIT)
        image,score = dart.dart_hit(image)
        if RM and DART_HIT:
            scoreboard.score=scoreboard.score+score
            score=0
            dart.dart_removed(image)
            CAPTURED=False
            DART_HIT=False
            RM = False
        '''if DART_FALLING and not dart.CAPTURED and not CAPTURED and not k==1 and RM:
            image,pointer_dart_falling,DART_FALLING = dart.dart_falling(image,pointer_dart_falling,pos_fall,DART_FALLING)
            if not DART_FALLING:
                pos_fall=(0,0)
            '''
        if p:
            image,pointer_dart_falling,DART_FALLING,p = dart.dart_falling(image,pointer_dart_falling,DART_FALLING,p)
        
        
        
        cv2.imshow('AIRD' , image)
        if (cv2.waitKey(1) & 0xFF == 27):
            break

cap.release()
cv2.destroyAllWindows()

#change
 