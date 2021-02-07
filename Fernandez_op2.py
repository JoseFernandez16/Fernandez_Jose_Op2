from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import FadeTransition, ScreenManager, Screen, WipeTransition
import pandas as pd
import pyttsx3
import speech_recognition 
import time
from conexion import *
from intento_1 import *

Builder.load_file('Fernandez_op2.kv')

Config.set('graphics', 'width', 800)
Config.set('graphics', 'height', 500)

#CONF KIVY
class ScreenExamen(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = WipeTransition()

    ##############################################################################################################
    ##############################################################################################################
    def cambio_reg(self,dt):
        self.ids.codigo.text   = str(self.cod)
        self.ids.nombre.text   = str(self.nom)  
        self.ids.apellido.text = str(self.ape) 
        self.ids.edad.text     = str(self.ed)
        self.ids.nota1.text    = str(self.n1)    
        self.ids.nota2.text    = str(self.n2)    
        self.ids.nota3.text    = str(self.n3)    
    
    def mod_reg(self,dt):
        self.ids.codigo_al.text = str(self.codigo_al)     
        self.ids.nota1_al.text  = str(self.nota1_al)    
        self.ids.nota2_al.text  = str(self.nota2_al)   
        self.ids.nota3_al.text  = str(self.nota3_al)

    def mostrar_estudiantes(self,dt):
        self.ids.registro.text = str(self.df_total)
    
    def cambio_label(self,dt):
        self.ids.estudiante.text = str(self.df_busqueda)

    ##############################################################################################################
    ##############################################################################################################
    def Registar_Alumno(self):

        engine=pyttsx3.init()
        engine.say("Complete los siguientes datos")
        engine.runAndWait()
        
        self.cod  = int(procesamientoVoz())
        self.nom  = str(procesamientoVoz())
        self.ape  = str(procesamientoVoz())
        self.ed   = int(procesamientoVoz())
        self.n1   = int(procesamientoVoz())
        self.n2   = int(procesamientoVoz())
        self.n3   = int(procesamientoVoz())
        self.prom = (self.n1+self.n2+self.n3)/3
        self.prom = round(self.prom,2)
        self.agre = Clock.schedule_once(self.cambio_reg)
        time.sleep(0.5)        
        insertar_datos(self.cod,self.nom,self.ape,self.ed,self.n1,self.n2,self.n3,self.prom)
        
    def Buscar_Alumno(self):
        self.code = int(self.ids.code.text)
        print(self.code)
        self.intento     = bus_estudiante(self.code)
        self.df_busqueda = pd.DataFrame(self.intento, columns=['Nombre','Apellido','No1','No2','No3','Promedio']).to_string(index=False)
        self.busqueda    = Clock.schedule_once(self.cambio_label)

    def Mostrar_Alumno(self):
        self.resp     = total_estudiantes()
        self.df_total = pd.DataFrame(self.resp, columns=['Codigo','Nombre','Apellido','Edad','No1','No2','No3','Promedio']).to_string(index=False)
        self.busqueda = Clock.schedule_once(self.mostrar_estudiantes)
        print(self.df_total)
    
    def Modificar_Alumno(self):
        engine = pyttsx3.init()
        engine.say("Complete los siguientes datos")
        engine.runAndWait()
        
        self.codigo_al  = int(procesamientoVoz())
        self.nota1_al   = int(procesamientoVoz())
        self.nota2_al   = int(procesamientoVoz())
        self.nota3_al   = int(procesamientoVoz())
        self.prom       = (self.nota1_al+self.nota2_al+self.nota3_al)/3
        self.prom_al    = round(self.prom,2)
        self.modi = self.evento2=Clock.schedule_once(self.mod_reg)
        time.sleep(0.5)        
        editar_datos(self.nota1_al,self.nota2_al,self.nota3_al,self.prom_al,self.codigo_al)

#FUNCIONES
def procesamientoVoz():
    reco = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("comenzó grabacion")
        cod= reco.listen(source)
        print("finalizó grabacion")
    time.sleep(1)
    val=(reco.recognize_google(cod,language="es"))
    return val

class ScreenApp(App):
    title = 'REGRISTO DE ESTUDIANTES'
    def build(self):
        return ScreenExamen()

if __name__=='__main__':
    ScreenApp().run()

"""
CREATE TABLE Alumnos (
	Codigo_al VARCHAR(4) PRIMARY KEY,
	Nombre_al VARCHAR(80) NOT NULL,
	Apellido_al VARCHAR(80) NOT NULL,
	Edad_al VARCHAR(3) NOT NULL,
	Nota1_al VARCHAR(3) NOT NULL,
	Nota2_al VARCHAR(3) NOT NULL,
	Nota3_al VARCHAR(3) NOT NULL,
	Promedio_al VARCHAR(6) NOT NULL
);"""