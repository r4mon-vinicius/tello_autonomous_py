import cv2
from djitellopy import Tello
import time

# inicializa e conecta com o Tello
tello = Tello()
tello.connect()
print(f"Bateria: {tello.get_battery()}%")
# comeca a transmissao de video
tello.streamon()
count = 0

while True: 
    # captura cada frame do objeto frame do tello
    frame = tello.get_frame_read().frame
    # converte o frame em RGB para BGR
    frame2 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame2 = cv2.resize(frame2, (544, 306))

    #exibe na tela 'Video' cada frame obtido no laço de repeticao
    cv2.imshow('Video', frame2) 
    # salva fotos da transmissao
    cv2.imwrite(f"movel{count}.jpeg", frame2)
    count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    # pequeno delay de 0.5 segundos entre cada laço de repeticao
    time.sleep(0.5)
# desliga a transmissao de video
tello.streamoff()
cv2.destroyAllWindows()
