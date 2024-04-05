import os
import cv2
import numpy as np
import face_recognition as fr
import imutils
from datetime import datetime
import random

path = './data2'
images = []
classes = []
lista = os.listdir(path)

comp1=100

for lis in lista:
    imgdb = cv2.imread(f'{path}/{lis}')
    images.append(imgdb)
    classes.append(os.path.splitext(lis)[0])


def codRostros(images):
    encodings = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodings.append(encode)
    return encodings

def horario(nombre):
    with open('Horario.csv', 'r+') as h:
        data = h.readlines()
        nombres = []
        for line in data:
            entry = line.split(',')
            nombres.append(entry[0])
        
        if nombre not in nombres:
            info =datetime.now()
            fecha = info.strftime('%Y-%m-%d')
            hora = info.strftime('%H:%M:%S')
            h.writelines(f'\n{nombre},{fecha},{hora}')
            print(info)

rostroscod = codRostros(images)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame2 = cv2.resize(frame, (0,0), None, 0.25, 0.25)
    rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    faces = fr.face_locations(rgb)
    facesCod = fr.face_encodings(rgb, faces)

    for facecod, faceloc in zip(facesCod, faces):
        comparacion = fr.compare_faces(rostroscod, facecod)
        simi = fr.face_distance(rostroscod, facecod)
        min = np.argmin(simi)
        if comparacion[min]:
            nombre = classes[min]
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            indice = comparacion.index(True)

            if comp1 != indice:
                r = random.randrange(0, 255, 50)
                g = random.randrange(0, 255, 50)
                b = random.randrange(0, 255, 50)

                comp1 = indice
            
            if comp1 == indice:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (r, g, b), 2)
                cv2.rectangle(frame, (x1, y2-35), (x2, y2), (r, g, b), cv2.FILLED)
                cv2.putText(frame, nombre, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                horario(nombre)

    cv2.imshow('frame', frame)
    t = cv2.waitKey(30)
    if t == 27:
        break



