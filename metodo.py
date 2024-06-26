import os
import cv2
import numpy as np
import face_recognition as fr
from datetime import datetime
import json

class FaceRecognition:
    def __init__(self, path):
        self.path = path
        self.images = []
        self.classes = []
        self.lista = os.listdir(self.path)
        self.comp1 = 100

    def load_images(self):
        for lis in self.lista:
            imgdb = cv2.imread(f'{self.path}/{lis}')
            self.images.append(imgdb)
            self.classes.append(os.path.splitext(lis)[0])

    def codRostros(self):
        encodings = []
        for img in self.images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = fr.face_encodings(img)[0]
            encodings.append(encode)
        return encodings

    def horario(self, nombre: str, datetime):
        with open('Horario.json', 'a+') as h:
            h.seek(0)
            data = h.read()
            if len(data) == 0:
                data = []
            else:
                data = json.loads(data)
            fecha = datetime.strftime('%Y-%m-%d')
            hora = datetime.strftime('%H:%M:%S')
            new_entry = {'nombre': nombre, 'fecha': fecha, 'hora': hora}
            data.append(new_entry)
            h.seek(0)
            h.truncate()
            json.dump(data, h, indent=4)

    def run(self):
        self.load_images()
        rostroscod = self.codRostros()
        cap = cv2.VideoCapture(0)

        start_time = None

        while True:
            ret, frame = cap.read()
            frame2 = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            faces = fr.face_locations(rgb)
            facesCod = fr.face_encodings(rgb, faces)

            for facecod, faceloc in zip(facesCod, faces):
                comparacion = fr.compare_faces(rostroscod, facecod)
                simi = fr.face_distance(rostroscod, facecod)
                min = np.argmin(simi)
                if comparacion[min]:
                    nombre = self.classes[min]
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    indice = comparacion.index(True)

                    if self.comp1 != indice:
                        self.comp1 = indice
                        start_time = datetime.now()

                    if self.comp1 == indice:
                        elapsed_time = datetime.now() - start_time
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (117, 243, 214), 2)
                        cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (117, 243, 214), cv2.FILLED)
                        cv2.putText(frame, nombre, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        if elapsed_time.total_seconds() >= 2:
                            cv2.destroyAllWindows()
                            return nombre, datetime.now()

            cv2.namedWindow('Reconocimiento', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('Reconocimiento', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow('Reconocimiento', frame)
            t = cv2.waitKey(30)
            if t == 27:
                break

