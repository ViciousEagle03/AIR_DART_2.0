import time
import cv2
class DartMech:
    def __init__(self,image,prev_distance_from_s,distance_hand_from_s,
                 DART_POS,current_time,start_time):
        self.prev_distance_from_s = prev_distance_from_s
        self.distance_hand_from_s = distance_hand_from_s
        self.DART_POS = DART_POS
        self.image = image
        self.current_time = current_time
        self.start_time = start_time
    def throw_dart(self):
        print(f'current_time{self.current_time}')
        print(f'start{self.start_time}')
        if self.prev_distance_from_s  -  self.distance_hand_from_s >20 :
            cv2.putText(self.image ,'yeah',self.DART_POS,
                        cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            self.prev_distance_from_s = self.distance_hand_from_s
            self.start_time=self.current_time
        info = [self.image , ]
        return()