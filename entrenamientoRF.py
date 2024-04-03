import cv2
import os
import numpy as np

class FaceRecognitionTrainer:
    def __init__(self):
        self.dataPath = './data'
        self.labels = []
        self.facesData = []
        self.peoleList = os.listdir(self.dataPath)
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label = 0

    def update_model(self):

        self.facesData = []
        for nameDir in self.peopleList:
            personPath = self.dataPath + '/' + nameDir
            print('Leyendo las imágenes')
            for fileName in os.listdir(personPath):
                self.labels.append(self.label)
                self.facesData.append(cv2.imread(personPath+'/'+fileName,0))
                image = cv2.imread(personPath+'/'+fileName,0)
            self.label = self.label + 1

        print('Entrenando...')
        self.face_recognizer.train(self.facesData, np.array(self.labels))
        print('Modelo entrenado exitosamente')
        self.face_recognizer.write('modeloLBPH.xml')
        cv2.destroyAllWindows()

