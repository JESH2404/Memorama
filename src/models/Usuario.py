# src/models/Usuario.py

class Usuario:
    def __init__(self, nombre, puntuacion=0, tiempo=0, dificultad=0):
        self.nombre = nombre
        self.puntuacion = puntuacion
        self.tiempo = tiempo
        self.dificultad = dificultad
