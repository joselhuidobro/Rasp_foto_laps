
#Codigo para tomar foto cada 5 segundos nombrarla  y guardarla en una carpeta en especifico con fecha de la captura. Despues se envia la imagen por un socket ZMQ

from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
import cv2
import base64

import zmq
import numpy as np



numeroFichero = 0
t = 5 #tiempo para tomar la fotografia
dia = 1



context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect('tcp://xx.xx.xx.xx:5555')



# iniciar
camera = PiCamera()
camera.resolution = (640, 480)

camera.framerate = 50
camera.hflip = True


while (True):

   today= datetime.now()
   dia = today.day
   mes = today.month
  
   print('Tomar foto!')
   numeroFichero= numeroFichero + 1
   
#---- toma la foto y la guarda en la raspi
   foto= camera.capture('/home/pi/Documents/fotolaps/dia3/FotoNo.%s_dia-%s_mes-%s.jpg'% (numeroFichero ,dia,mes)) ## lo comente para no ocupar espacio en memoria

#---- la manda por medio de socket a la PC local
   f = open('/home/pi/Documents/fotolaps/dia3/FotoNo.%s_dia-%s_mes-%s.jpg'% (numeroFichero ,dia,mes),'rb')
   bytes = bytearray(f.read())
   strng = base64.b64encode(bytes)
   socket.send(strng)
   f.close()


   while t: # Hasta que t vale cero
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1

   t = 5 #reset tiempo en sec para tomar la fotografia
