#Este fichero es el que tendra funciones auxiliares
import os
import platform
import re

def limpiar_pantalla():
    os.system('cls') if platform.system() == "Windows" else os.system('clear')

def leer_texto(longitud_min=0, longitud_max=100, mensaje=None):
    print(mensaje) if mensaje else None
    while True:
        texto = input("> ")
        if len(texto) < longitud_min or len(texto) > longitud_max:
            print(f"El texto debe tener entre {longitud_min} y {longitud_max} caracteres.")
            continue
        return texto

def dni_valido(dni, lista):
    if not re.match(r'[0,9]{2}[A-Z]$', dni):
        print("El DNI no es válido. Debe tener 8 dígitos y una letra.")
        return False
    for cliente in lista:
        if cliente.dni == dni:
            print("El DNI ya existe.")
            return False
    return True
