import cv2
import os
import imutils

class capturaRostros:
    def __init__(self, videoPath):
        self.dataPath = './data'
        if not os.path.exists(self.dataPath):
            os.makedirs(self.dataPath)
            print('Carpeta creada: ',self.dataPath)

        self.cap = cv2.VideoCapture(videoPath)
        self.faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        self.count = 0
    
    def capturar(self, personName):
        try:
            self.personPath = self.dataPath + '/' + personName
            if not os.path.exists(self.personPath) and personName != "":
                os.makedirs(self.personPath)
                print('Carpeta creada: ',self.personPath)
            elif personName == "":
                print('El nombre no puede estar vacío.')
                return
            if os.path.exists(self.personPath):
                add_count = len(os.listdir(self.personPath))
                self.count = self.count + add_count
            while True:
                ret, frame = self.cap.read()
                if ret == False: break
                frame = imutils.resize(frame, width=640)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                auxFrame = frame.copy()

                faces = self.faceClassif.detectMultiScale(gray,1.15,3)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    rostro = auxFrame[y:y+h,x:x+w]
                    rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
                    cv2.imwrite(self.personPath + '/rostro_{}.jpg'.format(self.count),rostro)
                    self.count = self.count + 1
                    print(self.count)
                cv2.imshow('frame',frame)
                k = cv2.waitKey(30)
                if k == 27 or self.count >= 300:
                    break

            self.cap.release()
            cv2.destroyAllWindows()
            return True
        except Exception as e:
            print(e)
            self.cap.release()
            cv2.destroyAllWindows()
            return False