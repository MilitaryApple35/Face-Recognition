import tkinter as tk
import entrenamientoRF
import capturaRostros
from tkinter import filedialog
from metodo2 import FaceRecognition


class App:
    def __init__(self):
        self.ruta_archivo = ""
        self.video_reconocer = ""
        # Crear la ventana
        self.ventana = tk.Tk()
        #ventana.attributes('-fullscreen', True)
        self.ventana.geometry("800x600")
        self.ventana.title("Captura de Rostro")

        # Etiqueta y campo de entrada para el nombre
        self.label_nombre = tk.Label(self.ventana, text="Nombre:")
        self.label_nombre.pack()
        self.entry_nombre = tk.Entry(self.ventana)
        self.entry_nombre.pack()
        self.label_ruta = tk.Label(self.ventana, text="Selecciona un archivo de video")
        self.label_ruta.pack()
        self.boton_archivo = tk.Button(text="Seleccionar archivo", command=self.seleccionar_archivo)
        self.boton_archivo.pack()
        # Botón para capturar el rostro
        self.boton_capturar = tk.Button(self.ventana, text="Capturar Rostro", command=self.validar_nombre)
        self.boton_capturar.pack()

        # Etiqueta para mostrar mensajes de error
        self.label_error = tk.Label(self.ventana, fg="red")
        self.label_error.pack()

        self.boton_reconocer1 = tk.Button(self.ventana, text="Reconocer rostro con camara", command=self.reconocer_rostro)
        self.boton_reconocer1.pack()
        self.label_ruta2 = tk.Label(self.ventana, text="Selecciona un archivo de video")
        self.label_ruta2.pack()
        self.boton_archivo2 = tk.Button(text="Seleccionar archivo", command=self.seleccionar_archivo2)
        self.boton_archivo2.pack()
        self.boton_reconocer2 = tk.Button(self.ventana, text="Reconocer rostro con video", command=self.reconocer_rostro2)
        self.boton_reconocer2.pack()
        self.label_error2 = tk.Label(self.ventana, fg="red")
        self.label_error2.pack()
        # Botón para salir
        self.boton_salir = tk.Button(self.ventana, text="Salir", command=self.ventana.destroy)
        self.boton_salir.pack()
        # Iniciar la ventana
        self.ventana.mainloop()
    
    def validar_nombre(self):
        print(self.ruta_archivo)
        nombre = self.entry_nombre.get()
        if nombre == "":
            self.label_error.config(text="El nombre no puede estar vacío.")
        elif self.ruta_archivo == "":
            self.label_error.config(text="Selecciona un archivo de video.")
        else:
            self.label_error.config(text="")
            captura = capturaRostros.capturaRostros(self.ruta_archivo)
            if captura.capturar(self.entry_nombre.get()):
                entrenar = entrenamientoRF.FaceRecognitionTrainer()
                entrenar.update_model()
    
    def seleccionar_archivo(self):
        self.ruta_archivo = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4;*.mov;*.avi;*.wmv;*.flv;*.mkv;*.3gp;*.webm")])
        if self.ruta_archivo != "":
            self.label_ruta.config(text=f"El video seleccionado es: {self.ruta_archivo}")
        

        
    def seleccionar_archivo2(self):
        self.video_reconocer = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4;*.mov;*.avi;*.wmv;*.flv;*.mkv;*.3gp;*.webm")])
        if self.video_reconocer != "":
            self.label_ruta2.config(text=f"El video seleccionado es: {self.video_reconocer}")

    def reconocer_rostro(self):
        reconocer = reconocimientoFacial.ReconocimientoFacial(0)
        reconocer.reconocer()
    
    def reconocer_rostro2(self):
        if self.video_reconocer == "":
            self.label_error2.config(text="Selecciona un archivo de video.")
        else:
            reconocer = reconocimientoFacial.ReconocimientoFacial(self.video_reconocer)
            self.label_error2.config(text="")
            reconocer.reconocer()


app = App()