import dearpygui.dearpygui as dpg
import csv
from metodo2 import FaceRecognition

def pass_list(sender, app_data):
    FaceRecognition().run()

def show_list(sender, app_data):
    with open('horario.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    with dpg.window(label="Lista"):
        dpg.add_table(header_row=data[0], rows=data[1:])

# def capture_face(sender, app_data):
    # Aquí debes implementar la lógica para capturar una nueva cara y guardarla en ./data2

dpg.create_context()
dpg.create_viewport(title='Pase de lista', width=600, height=300)

with dpg.window(label="Menu"):
    dpg.add_button(label="Pasar lista", callback=pass_list)
    dpg.add_button(label="Lista", callback=show_list)
    dpg.add_button(label="Capturar rostro nuevo") #callback=capture_face

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()