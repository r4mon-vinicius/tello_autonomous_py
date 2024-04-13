import random 
import time

class TelloMoves():
    def __init__(self, tello):
        self.tello = tello
        self.lr = 0
        self.fb = 0
        self.ud = 0
        self.yaw = 0
    
    def values(self):
        self.lr = random.randint(-40, 40)
        self.fb = random.randint(-40, 40)
        self.ud = random.randint(0, 20)
        self.yaw = random.randint(-40, 40)

        return [self.lr, self.fb, self.ud, self.yaw]
    
    def random_moves(self):
        count = 0
        values = []
        while count <= 5:
            values = self.random_moves()
            self.tello.send_rc_control(values[0], values[1], values[2], values[3])
            print(f"COUNT: {count}")
            count += 1
    
            time.sleep(1.5)
 
    
    
