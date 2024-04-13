from djitellopy import Tello
import cv2
import time

class BatteryError(Exception):
    def __init__(self, mensagem):
        self.mensagem = mensagem

def battery_error(tello_battery):
    if tello_battery < 15:
        raise BatteryError("Bateria menor que 15%, operação cancelada.")

def calculate_fps():
    num_frames = 0
    start_time = time.time()
    fps = 0
    font = cv2.FONT_HERSHEY_SIMPLEX


class TelloZune(Tello):
    def __init__(self):
        super().__init__()
    
    def initiate_tello(self):
        self.connect()
        try: 
            battery_error(self.get_battery())
            self.streamon()
            self.takeoff()
            self.send_rc_control(0, 0, 0, 0)

        except BatteryError as erro:
            print(erro.mensagem)

    def initiate_video(self):
        while True:
            self.frame = self.get_frame_read().frame
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR)
            self.frame = cv2.resize(self.frame, (544, 306))

            cv2.imshow('Video tello', self.frame)
            if cv2.waitKey(1) == ord('q'):
                break
            
    
