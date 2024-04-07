import base64
import io
import eel
import eel.browsers
from metodo import FaceRecognition
import json
from datetime import datetime
from PIL import Image

frg = FaceRecognition('./data')

@eel.expose
def tomar_lista():
    print('Tomando lista')
    try:
        dt : datetime
        name, dt= frg.run()
        print (name, dt)
        fecha = dt.strftime('%Y-%m-%d')
        hora = dt.strftime('%H:%M:%S')
    except Exception as e:
        print(e)
        return None, None, None, None
    return name, fecha, hora, dt

@eel.expose
def get_data():
    data = json.loads(open('Horario.json').read())
    return data

@eel.expose
def process_image(data, nombre):
    # Convierte la imagen de base64 a bytes
    image_data = base64.b64decode(data.split(',')[1])
    # Abre la imagen con PIL
    image = Image.open(io.BytesIO(image_data))
    # Guarda la imagen en la carpeta data
    image.save(f'./data/{nombre}.png')

@eel.expose
def confirmar_lista(name, datetime):
    frg.horario(name, datetime)


eel.init('web')
eel.start('index.html', cmdline_args=['--start-fullscreen'])
