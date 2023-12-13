import mediapipe as mp
import cv2
import math
import time
import numpy as np
from Score_board import Scoreboard
from dart import Dart
from constants import CAM_RES


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
    
    return distanceCM

def power_of_throw(coord_1,coord_2):
    x1,y1  = coord_1
    x2,y2  = coord_2
    distance  = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    pow_throw = A1*distance**2 + B1*distance + C1
    
    return pow_throw

def distance_8and4(coord_1,coord_2):
    x1,y1  = coord_1
    x2,y2  = coord_2
    distance  = int(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    distance8and4 = A2*distance**2 + B2*distance + C2
    return distance8and4

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


#mp.solutions is a module that provides a set of pre-built solutions
#for various computer vision and machine learning tasks. 
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,CAM_RES[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,CAM_RES[1])
cv2.namedWindow("AIRD",cv2.WND_PROP_FULLSCREEN)

dart = Dart()

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
        
        image = cv2.cvtColor(image , cv2.COLOR_RGB2BGR)
    
        
        image = dart.set_bg(image)
        image_dart,dart_number=dart.dart_display(image)
        if dart_number>0:
            image = image_dart
        dart.allow_grab(allowgrab)
        image = dart.dart_board(image)

        
        if results.multi_hand_landmarks:
            for num,finger in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image , finger , mp_hands.HAND_CONNECTIONS)
            index_finger_tip = finger.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            reference_point = (0,0)
            thumb_finger_tip = finger.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_mcp = finger.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            pinky_mcp = finger.landmark[mp_hands.HandLandmark.PINKY_MCP]
            wrist = finger.landmark[mp_hands.HandLandmark.WRIST]
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
    
            distance_hand_from_s= distance_from_screen(index_finger_mcp_coord,pinky_finger_mcp_coord)
            power_throw = power_of_throw(index_finger_coord,wrist_coord)
            power_throw = power_throw*2
            distance_throw = distance_8and4(index_finger_coord,thumb_coord)
            INTERVAL =0.2
            current_time = time.time()
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
                
            elif(distance>50 and distance<100 and not CAPTURED and threw_dart<10):
                if not CAPTURED and not k==1 and dart.CAPTURED:
                    dart.dart_removed(image)
                    p=True
                    DART_FALLING = True
                    pointer_dart_falling =0
                    pos_fall = coord
                CAPTURED=False
            
            cv2.putText(image ,f'power : {power}',(40,40),
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.putText(image,f'distance{distance}',(40,60),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.putText(image,f'power/{int(power)}',(40,80),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.putText(image,f'disth_from_s/{int(distance_hand_from_s)}',(40,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            
        if k==1 and not CAPTURED:
            image,DART_HIT,allowgrab,pointer_dart,k = dart.resizing(pointer_dart,
                                                                    image,DART_HIT)
        image = scoreboard.display_scoreboard(image,DART_HIT)
        image,score = dart.dart_hit(image)
        if RM and DART_HIT:
            scoreboard.up_score(score)
            cv2.putText(image,f'score/{scoreboard.score}',(40,120),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            score=0
            dart.dart_removed(image)
            CAPTURED=False
            DART_HIT=False
            RM = False
        if p:
            image,pointer_dart_falling,DART_FALLING,p = dart.dart_falling(image,pointer_dart_falling,DART_FALLING,p)
            
        cv2.imshow('AIRD' , image)
        if (cv2.waitKey(1) & 0xFF == 27):
            break

cap.release()
cv2.destroyAllWindows()


 