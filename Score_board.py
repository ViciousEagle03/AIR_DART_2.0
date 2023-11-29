import cv2
import cvzone
import math
from constants import MY_RESOLUTION__X,MY_RESOLUTION__Y,DART_BOARD_SIZE,CAM_RES
class Scoreboard:
    def __init__(self) -> None:
        self.score = 0
        self.inside_hit=False
    def up_score(self,score):
            self.score=score
            """breakpoint()"""
    def display_scoreboard(self,image,hit):
        
        self.hit = hit
        self.image = image
        self.display_image = cv2.putText(self.image,f'SCORE{self.score}',
                                         (int(MY_RESOLUTION__X*0.5),int(MY_RESOLUTION__Y*0.05)),
                                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        return self.display_image
    
    def in_dart_board(self,dart_hit):
        radius_dart_board = DART_BOARD_SIZE[0]//2 -50
        #50 is subtracted from radius because the outer layer of dart board has not been included in the image displayed
        dist_from_centre = math.sqrt((dart_hit[0] - CAM_RES[0]//2)**2 + (dart_hit[1] - CAM_RES[1]//2)**2)
        print(radius_dart_board)
        print(dist_from_centre)
        if dist_from_centre < radius_dart_board//4:
            self.score=5
            return (True)
        elif dist_from_centre < radius_dart_board//3:
            self.score=4
            return (True)
        elif dist_from_centre < radius_dart_board//2:
            self.score=2
            return (True)
        elif dist_from_centre < radius_dart_board:
            self.score=1
            return (True)
        else:
            return (False)
        #elif (CAM_RES[0]//2 - DART_BOARD_SIZE[0]//2 )<dart_pos[0]<(CAM_RES[0]//2 - DART_BOARD_SIZE[0]//2) and dart_pos[1]<(CAM_RES[1]//2 - DART_BOARD_SIZE[1]//2) :
        
     