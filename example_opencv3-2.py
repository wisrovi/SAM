from OpenCV_3 import OpenCV_3
detecFaces = OpenCV_3()
detecFaces.setConfianzaDeteccion(0.40)

import cv2

resolucionCamara = {
    "hd" : (1366,768),      #HD
    "720p" : (1280,720),    #HD+
    "1080p" : (1920,1080),  #full HD
    "1440p" : (2560,1440),  #QHD o 2K
    "UHD" : (3840,2160),
    "8K" : (7680,4320)
}
cam_port = 0
cap = cv2.VideoCapture(cam_port)
cap.set(3, resolucionCamara["UHD"][0]) 
cap.set(4, resolucionCamara["UHD"][1]) 
cap.read()


from functools import wraps
from time import time
def calcularTiempoo(f):
    @wraps(f)
    def cronometro(*args, **kwargs):
        t_inicial = time()
        salida = f(*args, **kwargs)
        t_final = time()
        print("Tiempo necesario este proceso: {} (segundos)".format(t_final - t_inicial))
        return salida
    return cronometro

@calcularTiempoo
def posicionarRostros(frame):
    listadoCoordenadasRostro = detecFaces.detectarRostros(frame)
    for (startX, startY, endX, endY, confianzaEsteRostro) in listadoCoordenadasRostro:
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
        
        text = "R: " + "{:.2f}%".format(confianzaEsteRostro * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    return frame

while True:
    ret, frame = cap.read()
    
    if ret:
        frame = posicionarRostros(frame)
            
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF 
    if key == ord("q"):
        break
cv2.destroyAllWindows()