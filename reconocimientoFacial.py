import cv2
import os

class ReconocimientoFacial:
    def __init__(self, videoPath):
        self.dataPath = './data'
        self.imagePaths = os.listdir(self.dataPath)
        print('imagePaths=', self.imagePaths)

        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        try:
            self.face_recognizer.read('modeloLBPH.xml')  # Try loading existing model
            print("Cargado modelo LBPH existente")
        except Exception as e:
            print("No existe modelo LBPH previo. Entrenar un nuevo modelo antes de la detección.")
            # Exit or provide instructions for initial model training
            exit()
        self.cap = cv2.VideoCapture(videoPath)
        self.faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

    def reconocer(self):
        while True:
            ret, frame = self.cap.read()
            if ret == False:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()

            faces = self.faceClassif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                rostro = auxFrame[y:y+h, x:x+w]
                rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                result = self.face_recognizer.predict(rostro)

                cv2.putText(frame, '{}'.format(result), (x, y-5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

                if result[1] <= 80:  # Adjust threshold as needed for LBPH
                    cv2.putText(frame, '{}'.format(self.imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                else:
                    cv2.putText(frame, 'No Reconocido', (x, y-20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            if k == 27:
                cv2.destroyAllWindows()
                break
