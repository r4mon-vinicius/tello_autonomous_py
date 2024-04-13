from utils import *
import numpy as np
import cv2
import time

Width = 544
Height = 306
#coordenadas do centro
CenterX = Width // 2
CenterY = Height // 2
#erro anterior
prevErrorX = 0
prevErrorY = 0
#coeficiente proporcional (obtido testando)
#determina o quanto a velocidade deve mudar em resposta ao erro atual
Kp = 0.35
#coeficiente derivativo (obtido testando)
#responsável por controlar a taxa de variação do erro
Kd = 0.35
speedFoward = 0

tello = initializeTello()
tello.takeoff()
tello.send_rc_control(0, 0, 0, 0)

while True:

    frame = getFrameTello(tello, (544, 306))
    frame, x1, y1, x2, y2, detections = baseDetect(frame) 

    detectWidth = x2 - x1
    cxDetect = (x2 + x1) // 2
    cyDetect = (y2 + y1) // 2

    #PID - Speed Control
    
    #se o centro da detecção encontrar-se na esquerda, o erro  na horizontal será negativo
    #se o objeto estiver na direita, o erro será positivo
    if (detections > 0):
        errorX = cxDetect - CenterX
        errorY = CenterY - cyDetect
        
        if (detectWidth < 400):
            speedFoward = 30
        else:
            speedFoward = 0
    else:
        errorX = 0
        errorY = 0
        speedFoward = 0

    #velocidade de rotação em torno do próprio eixo é calculada em relação ao erro horizontal
    speedYaw = Kp*errorX + Kd*(errorX - prevErrorX)
    speedUD = Kp*errorY + Kd*(errorY - prevErrorY)
    #não permite que a velocidade 'vaze' o intervalo -100 / 100
    speedYaw = int(np.clip(speedYaw,-100,100))
    speedUD = int(np.clip(speedUD,-100,100))

    #print(f'Speed: {speedFoward}')
    
    if(detections != 0):
        tello.send_rc_control(0, speedFoward, speedUD, speedYaw)
    else:
        tello.send_rc_control(0, 0, 0, 0)
    #o erro atual vira o erro anterior
    prevErrorX = errorX
    prevErrorY = errorY
    #time.sleep(0.7)

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) == ord('q'):
        tello.land()
        break

tello.streamoff()
cv2.destroyAllWindows()

