import math
import cv2
import numpy as np
import cvzone
from Score_board import Scoreboard
from constants import MY_RESOLUTION__X, MY_RESOLUTION__Y, DART_SIZE,DART_SIZE2,DART_SIZE1,CAM_RES,NUMBER_OF_DARTS,WIND_SIZE,DART_BOARD_SIZE
class Dart:

    
    def __init__(self) -> None:
        self.number_of_darts=[0,1,2,3,4]
        self.scoreboard = Scoreboard()
        darthit0 = cv2.imread("mediapipetest/struck_dart-removebg-preview .png",cv2.IMREAD_UNCHANGED)
        self.darthit = cv2.resize(darthit0,DART_SIZE2)
        self.dartboard0 = cv2.imread("mediapipetest/imagedartboard-removebg-preview.png",cv2.IMREAD_UNCHANGED)
        self.dartboard_pos = ((CAM_RES[0]//2 + DART_BOARD_SIZE[0]//2),(CAM_RES[1]//2 + DART_BOARD_SIZE[1]//2))
        self.darthit_number = [1,1,1,1,1]
        self.CAPTURED = False
        self.number = []
        self.allowgrab=True
        self.count=-1
        self.darts = [] 
        self.resize=1 
        self.pos_fall=(0,0)
        self.dart_captured_number=-12
        self.distance_throw = 0
        self.distancediff = 0
        self.anti_grav_pointer=10
        self.angle_of_throw=0
        self.intensity = 3
        self.pointer_wind = 0
        self.wind_pos=((100,200),(100,200),(100,200),(100,200),(100,200),(500,500),(500,500),(500,500),(500,500),(500,500),(500,200),(500,200),(500,200),(500,200),(500,200))
        #positions = [(int(MY_RESOLUTION__X * 0.1), int(MY_RESOLUTION__Y * 0.05)),
        #             (int(MY_RESOLUTION__X * 0.15), int(MY_RESOLUTION__Y * 0.05)),
        #            (int(MY_RESOLUTION__X * 0.20), int(MY_RESOLUTION__Y * 0.05))]
        self.positions = [(int(MY_RESOLUTION__X * 0.05), int(MY_RESOLUTION__Y * 0.05)),
                          (int(MY_RESOLUTION__X * 0.15), int(MY_RESOLUTION__Y * 0.05)),
                          (int(MY_RESOLUTION__X * 0.20), int(MY_RESOLUTION__Y * 0.05)),
                          (int(MY_RESOLUTION__X * 0.25), int(MY_RESOLUTION__Y * 0.05)),
                          (int(MY_RESOLUTION__X * 0.30), int(MY_RESOLUTION__Y * 0.05))]
        #for pos in positions:
             #self.darts.append(self.dart_create(self.image, pos))
        #self.darts.append(self.dart_create(positions))
        self.darthit_pos =[(0,0),(0,0),(0,0),(0,0),(0,0)]

    def dart_display(self,image):
        self.count=-1
        self.number.clear()
        for pos in self.positions:
            self.count+=1
            self.number.append(self.count)
            dart_img = cv2.imread("dart_png.png", cv2.IMREAD_UNCHANGED)
            self.dart_img1 = cv2.resize(dart_img, DART_SIZE)
            if self.CAPTURED and (self.dart_captured_number == self.count):
                self.dart = image
            else:
                self.dart = cvzone.overlayPNG(image, self.dart_img1, pos)
        print(f'no .of darts{self.count}')
        return (self.dart,len(self.positions))
        
    
    def check_movement(self,coord):
        
        
        #distance = math.dist((positions[0]*CAM_RES[0] , positions[1]*CAM_RES[1]) 
        #                        , (coord[0]*CAM_RES[0] ,coord[1]*CAM_RES[1]))
        if not self.CAPTURED and self.allowgrab:
            count=int(-1)
            print(len(self.positions))
            for pos in self.positions:
                count+=1
                if  pos[0]< coord[0]<pos[0]+ DART_SIZE[0] and pos[1]<coord[1]<pos[1]+DART_SIZE[1] or self.CAPTURED:
                    self.CAPTURED = True
                    self.dart_captured_number=count
                    print(self.dart_captured_number)
                    print('------------------------------')
                    return self.CAPTURED
        print(self.number)
        print(self.CAPTURED)  
        print(self.dart_captured_number)
        if self.CAPTURED and (self.dart_captured_number in self.number) and self.allowgrab:
            print("moving dart...........")
            position_captured = self.positions[self.dart_captured_number]
            self.positions[self.dart_captured_number] = coord
            pos = position_captured
            print(self.positions)
            if  pos[0]< coord[0]<pos[0]+ DART_SIZE[0] and pos[1]<coord[1]<pos[1]+DART_SIZE[1] or self.CAPTURED:
                    return self.CAPTURED
            
       
        
    def moved(self,frame,coord) :
        if self.dart_captured_number in self.number and self.allowgrab:
            new_pos =(coord[0] - DART_SIZE[0] //2, coord[1] - DART_SIZE[1]//2)
            print(self.dart_captured_number)
            self.positions[self.dart_captured_number] == new_pos
            print(f'lolololol{self.positions}')
            image = cvzone.overlayPNG(frame,self.dart_img1,new_pos)  
            return(image,new_pos)
        else:
            return(frame,coord)

    def dart_removed(self,frame):
        self.CAPTURED=False
        self.resize=1
        
        for number in self.number:
            if self.dart_captured_number == number:
                self.pos_fall = self.positions[self.dart_captured_number]
                self.number.remove(self.dart_captured_number) 
                self.positions[number]=[10000,10000]
                self.positions.remove(self.positions[number])
                print("YES")
                print(self.dart_captured_number)
                image = cvzone.overlayPNG(frame,self.dart_img1,[1000,1000])
                return(image)

    def dart_animate(self,frame,pointer_dart,dart_pos):
        dart_animate_01 = cv2.imread("dart_animate/Dart_1-rbg.png",cv2.IMREAD_UNCHANGED)
        dart_animate_1 = cv2.resize(dart_animate_01 , DART_SIZE)
        dart_animate_02 = cv2.imread("dart_animate/Dart_2-rbg.png",cv2.IMREAD_UNCHANGED)
        dart_animate_2 = cv2.resize(dart_animate_02 , DART_SIZE)
        dart_animate_03 = cv2.imread("dart_animate/Dart_3-rbg.png",cv2.IMREAD_UNCHANGED)
        dart_animate_3 = cv2.resize(dart_animate_03 , DART_SIZE)
        dart_animate_03 = cv2.imread("dart_animate/Dart_3-rbg.png",cv2.IMREAD_UNCHANGED)
        dart_animate_list = (dart_animate_1,dart_animate_2,dart_animate_3)
            
        self.allowgrab = False
        
        self.DART_RESIZE = int(DART_SIZE[0] * self.resize),int(DART_SIZE[1]*self.resize)
        dart_pos1 = (dart_pos[0]-self.DART_RESIZE[0]//2,dart_pos[1]-self.DART_RESIZE[1]//2)
        
        animate_dart = cv2.resize(dart_animate_list[pointer_dart],self.DART_RESIZE)
        image = cvzone.overlayPNG(frame ,animate_dart,dart_pos1)
        self.resize = self.resize - 0.03
        return(image)
    
        
    def allow_grab(self,allowgrab):
        self.allowgrab = allowgrab
        
    

    
    
    def resizing(self,pointer_dart,image,DART_HIT):
        print(f'........................{self.positions}')
        if self.resize>=0.02:
            k=1
            if pointer_dart == 3:
                pointer_dart=0
            if  self.positions :
                self.positions[self.dart_captured_number] = self.wind_blow()
                self.positions[self.dart_captured_number] =self.grav1()
                image = self.dart_animate(image,pointer_dart,self.positions[self.dart_captured_number])
                
            pointer_dart+=1
        self.allowgrab=False
                
        
        if self.resize<=0.2:
            DART_HIT = True
            k=0 
            self.allowgrab = True
            self.anti_grav_pointer=10
            self.darthit_number[self.dart_captured_number] = 0
            self.darthit_pos[self.dart_captured_number]=self.positions[self.dart_captured_number]
        return(image , DART_HIT,self.allowgrab,pointer_dart,k)
        
        
    def captured(self):
        return self.CAPTURED
    
    def dart_falling_animate(self,frame,pointer_dart_fall):
            dart_fall_01 = cv2.imread("mediapipetest/falling_dart1/Untitled_design__2_-removebg-preview.png",cv2.IMREAD_UNCHANGED)
            dart_fall_02 = cv2.imread("mediapipetest/falling_dart1/Untitled_design__3_-removebg-preview.png",cv2.IMREAD_UNCHANGED)
            dart_fall_03 = cv2.imread("mediapipetest/falling_dart1/Untitled_design__4_-removebg-preview.png",cv2.IMREAD_UNCHANGED)
            dart_fall_04 = cv2.imread("mediapipetest/falling_dart1/Untitled_design__5_-removebg-preview.png",cv2.IMREAD_UNCHANGED)
            dart_fall_05 = cv2.imread("mediapipetest/falling_dart1/Untitled_design__6_-removebg-preview.png",cv2.IMREAD_UNCHANGED)
            dart_fall_06 = cv2.imread("mediapipetest/falling_dart1/Untitled_design__7_-removebg-preview.png",cv2.IMREAD_UNCHANGED)
            dart_fall_1 = cv2.resize(dart_fall_01 , DART_SIZE1)
            dart_fall_2 = cv2.resize(dart_fall_02 , DART_SIZE1)
            dart_fall_3 = cv2.resize(dart_fall_03 , DART_SIZE1)
            dart_fall_4 = cv2.resize(dart_fall_04 , DART_SIZE1)
            dart_fall_5 = cv2.resize(dart_fall_05 , DART_SIZE1)
            dart_fall_6 = cv2.resize(dart_fall_06 , DART_SIZE1)
            self.pos_fall = (self.pos_fall[0],self.pos_fall[1]+25)
            falling_dart_list = (dart_fall_1,dart_fall_2,dart_fall_3,dart_fall_4,dart_fall_5,dart_fall_6)
            f_dart = falling_dart_list[pointer_dart_fall]
            image = cvzone.overlayPNG(frame,f_dart,self.pos_fall)
            return(image,self.pos_fall)
    
    def dart_falling(self,image,pointer_dart_falling,DART_FALLING,p):
        if self.pos_fall[1]<=1000 :
            p=True
            pointer_dart_falling+=1
            if pointer_dart_falling==6:
                pointer_dart_falling=0
             
            image,self.pos_fall = self.dart_falling_animate(image,pointer_dart_falling)
            return (image,pointer_dart_falling,DART_FALLING,p)
        else:
            p=False
            return (image,pointer_dart_falling,DART_FALLING,p)
    # The inclusion of gravity in darts    
    # distance --> speed
    #
    def grav(self,distance_throw , power,distancediff ):
        if distance_throw >260 :
           pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] +15 )
           return pos
        elif distance_throw>200:
            pass
        elif distance_throw> 130:
            pass
        else:
            
    
            pass
    def grav2(self,distance_throw,distancediff,angle_of_throw):
        self.distance_throw = distance_throw
        self.distancediff = distancediff
        self.angle_of_throw = angle_of_throw
        
    '''def grav1(self):
        if self.distancediff >40 :
            if self.angle_of_throw>190:
                if self.anti_grav_pointer>1 :
                    pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -15 )
                    self.anti_grav_pointer-=1
                    return(pos)
            if self.angle_of_throw>100:
                if self.anti_grav_pointer>1 :
                    pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -5 )
                    self.anti_grav_pointer-=1
                    return(pos)
            if self.angle_of_throw<50:
                if self.anti_grav_pointer>1 :
                    pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -2 )
                    self.anti_grav_pointer-=1
                    return(pos)
            if self.distance_throw>260:
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] + 10 )
                return(pos)
            elif self.distance_throw >150:
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] + 8 )
                return(pos)
            elif self.distance_throw >100:
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] + 10 )
                return(pos)
        elif self.distancediff>35 :
            if self.anti_grav_pointer>4 :
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -3 )
                self.anti_grav_pointer-=1
                return(pos)
            if self.distance_throw>260:
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] + 3 )
                return(pos)
            elif self.distance_throw >150:
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] + 4 )
                return(pos)
            elif self.distance_throw >100:
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] + 6 )
                return(pos)
        elif self.distancediff >25:
            if self.distance_throw>260:
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] + 3 )
                return(pos)
            elif self.distance_throw >150:
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] + 6 )
                return(pos)
            elif self.distance_throw >100:
                pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] + 9 )
                return(pos)
            '''
            
            
    def grav1(self):
        if self.distancediff >45 :
            if self.distance_throw>260:
                if self.angle_of_throw>190:
                    if self.anti_grav_pointer>1 :
                        pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -15 )
                        self.anti_grav_pointer-=1
                        return(pos)
                    elif self.angle_of_throw>100:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -10 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    elif self.angle_of_throw<50:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -8 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] +3 )
                    return(pos)
            elif self.distance_throw >150:
                if self.angle_of_throw>190:
                    if self.anti_grav_pointer>1 :
                        pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -12 )
                        self.anti_grav_pointer-=1
                        return(pos)
                    if self.angle_of_throw>100:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -7 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    if self.angle_of_throw<50:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -5 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] +3 )
                    return(pos)
        elif self.distancediff>35 :
            if self.distance_throw>260:
                if self.angle_of_throw>190:
                    if self.anti_grav_pointer>1 :
                        pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -10 )
                        self.anti_grav_pointer-=1
                        return(pos)
                    if self.angle_of_throw>100:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -7 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    if self.angle_of_throw<50:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -5 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] +3 )
                    return(pos)
            elif self.distance_throw >150:
                if self.angle_of_throw>190:
                    if self.anti_grav_pointer>1 :
                        pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -8 )
                        self.anti_grav_pointer-=1
                        return(pos)
                    if self.angle_of_throw>100:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -5 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    if self.angle_of_throw<50:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -3 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] +3 )
                    return(pos)
            
        elif self.distancediff >25:
            if self.distance_throw>260:
                if self.angle_of_throw>190:
                    if self.anti_grav_pointer>1 :
                        pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -7 )
                        self.anti_grav_pointer-=1
                        return(pos)
                    if self.angle_of_throw>100:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -5 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    if self.angle_of_throw<50:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -2 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] +3 )
                    return(pos)
                
            elif self.distance_throw >150:
                if self.angle_of_throw>190:
                    if self.anti_grav_pointer>1 :
                        pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -6 )
                        self.anti_grav_pointer-=1
                        return(pos)
                    if self.angle_of_throw>100:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -4 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    if self.angle_of_throw<50:
                        if self.anti_grav_pointer>1 :
                            pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] -1 )
                            self.anti_grav_pointer-=1
                            return(pos)
                    pos =(self.positions[self.dart_captured_number][0],self.positions[self.dart_captured_number][1] +3 )
                    return(pos)

    def wind_blow(self):
        pos =(self.positions[self.dart_captured_number][0] -self.intensity ,self.positions[self.dart_captured_number][1] )
        return pos
                           
        
    def wind_animate(self,image):
        wind01 = cv2.imread("mediapipetest/windblow/windblow1.png",cv2.IMREAD_UNCHANGED)
        wind02 = cv2.imread("mediapipetest/windblow/windblow2.png",cv2.IMREAD_UNCHANGED)
        wind03 = cv2.imread("mediapipetest/windblow/windblow3.png",cv2.IMREAD_UNCHANGED)
        wind1 = cv2.resize(wind01 , WIND_SIZE)
        wind2 = cv2.resize(wind02 , WIND_SIZE)
        wind3 = cv2.resize(wind03 , WIND_SIZE)
        wind_list = (wind1,wind1,wind1,wind1,wind1,wind2,wind2,wind2,wind2,wind2,wind3,wind3,wind3,wind3,wind3)
        self.pointer_wind+=1
        if self.pointer_wind ==15:
            self.pointer_wind =0
        print(self.pointer_wind)
        
        image1 = cvzone.overlayPNG(image,wind_list[self.pointer_wind],self.wind_pos[self.pointer_wind])
        return image1

    def dart_board(self,image):
        
        image = cvzone.overlayPNG(image,self.dartboard0,((CAM_RES[0]//2 - DART_BOARD_SIZE[0]//2),(CAM_RES[1]//2 - DART_BOARD_SIZE[1]//2)))
        return image
    def dart_hit(self,image):
        score = 0
        for number in self.number_of_darts:  
            if self.darthit_number[number] == 0:
                print(f"number............{number}")
                if self.scoreboard.in_dart_board(self.darthit_pos[number]):
                    score = score + self.scoreboard.score
                    image = cvzone.overlayPNG(image,self.darthit,((self.darthit_pos[number][0] - DART_SIZE2[0]//2),(self.darthit_pos[number][1] - DART_SIZE2[1]//2)))
        return (image,score)
    
    def set_bg(self,image):
        bg_image = cv2.imread("mediapipetest/bg_dart.png",cv2.IMREAD_UNCHANGED)
        bg_image1 = cv2.resize(bg_image,DART_SIZE)
        image = cvzone.overlayPNG(image,bg_image,(500,500))
        return image
    