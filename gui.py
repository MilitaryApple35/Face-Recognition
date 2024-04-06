import eel
from metodo2 import FaceRecognition
import json
import os

frg = FaceRecognition('./data2')

@eel.expose
def tomar_lista():
    frg.run()
    

eel.init('web')
eel.start('index.html')