import cv2
import cvzone
from constants import MY_RESOLUTION__X,MY_RESOLUTION__Y,DART_BOARD_SIZE,CAM_RES
class Scoreboard:
    def __init__(self) -> None:
        self.score = 0
    def up_score(self):
        if self.hit:
            self.score+=1
    def display_scoreboard(self,image,hit):
        
        self.hit = hit
        self.image = image
        self.display_image = cv2.putText(self.image,f'SCORE{self.score}',
                                         (int(MY_RESOLUTION__X*0.6),int(MY_RESOLUTION__Y*0.05)),
                                            cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        return self.display_image
    
    def up_score(self,dart_pos):
        if(dart_pos[0]<(CAM_RES[0]//2 - DART_BOARD_SIZE[0]//2) and dart_pos[1]<(CAM_RES[1]//2 - DART_BOARD_SIZE[1]//2)):
            self.score+=10
        #elif (CAM_RES[0]//2 - DART_BOARD_SIZE[0]//2 )<dart_pos[0]<(CAM_RES[0]//2 - DART_BOARD_SIZE[0]//2) and dart_pos[1]<(CAM_RES[1]//2 - DART_BOARD_SIZE[1]//2) :
        
        