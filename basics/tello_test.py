from djitellopy import Tello
import cv2
import time
# Inicializa a captura de vídeo da webcam
#cap = cv2.VideoCapture(0)  # Use o índice da sua câmera se não for a padrão (0)
tello = Tello()
tello.connect()
tello.streamon()
# Variáveis para cálculo de FPS
frame_count = 0
start_time = time.time()

#cap = cv2.VideoCapture(0)

while True:
    # Captura um frame da webcam
    #ret, webcam = cap.read()
    tello_video = tello.get_frame_read().frame
    # Se a captura falhar, sai do loop
    #if not ret:
    #   break
    # Processamento do frame aqui (caso seja necessário)

    # Incrementa o contador de frames
    frame_count += 1
    #Calcula o FPS a cada segundo
    tempo = time.time() - start_time

    if tempo >= 1:
        fps = frame_count / (tempo)
        print(f"fps: {fps:.2f}")
        frame_count = 0
        start_time = time.time()
 
    # Exibe o frame capturado
    #cv2.imshow('Webcam', webcam)
    #print(webcam.get(cv2.CAP_PROP_FRAME_COUNT))
    cv2.imshow("Tello", tello_video)

    # Sai do loop se pressionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura e fecha a janela OpenCV
#cap.release()
tello.streamoff()
cv2.destroyAllWindows()