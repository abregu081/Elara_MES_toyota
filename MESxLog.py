# Marzo. Abregu Tomas para proyecto Harman/Toyota. Mirgor

# Version 1.1 (De a poco):
#   - Solo mantiene las funciones para BREQ/BCNF, BCMP/BACK.
#   - Se quita el ciclo con input() y while True en el main.

import socket
import datetime
import sys
import time
from collections import deque
import os

# ------------------------------------------------------------
# Variables globales y lectura de configuración
# ------------------------------------------------------------
current_directory = os.path.dirname(os.path.abspath(__file__))
setting_file = os.path.join(current_directory, 'setting.cfg')

# Para cargar la configuración al importar
setting = {}
titulos = {}

def read_setting(file):
    """
    Lee un archivo de configuración clave=valor.
    Ignora líneas en blanco o con #.
    """
    cfg = {}
    if not os.path.isfile(file):
        print("Warning: No se encontró setting.cfg en:", file)
        return cfg

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                cfg[key.strip()] = value.strip()
    return cfg

def load_titles():
    global titulos
    titulos.clear()  # Limpia los títulos anteriores
    try:
        with open("Labels.cfg", "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                titulos[key] = value
    except Exception as e:
        print(f"No se pudo cargar el archivo Labels.cfg: {e}")

def load_settings():
    global setting
    setting.clear()  # Limpia la configuración anterior
    
    try:
        with open("setting.cfg", "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                setting[key] = value

        print("Configuración recargada:", setting)  

    except Exception as e:
        print(f"Error al cargar configuración: {e}")

def printand(data):
    """
    Imprime información de seguimiento si 'tracelog' está activo en la config.
    """
    if setting.get('tracelog') == "1":
        print(str(data))

def send_message(ip, port, msg):
    """
    Envía un mensaje (string) al servidor SIM usando socket TCP.
    Agrega un salto de línea al final.
    Retorna la respuesta recibida como string.
    """
    timeout = int(setting.get('timeout_mes', 30))
    try:
    
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(timeout)
        client_socket.connect((ip, int(port)))
    except Exception as e:
        print("Hostname no habilitado por IT ")


    print(f"Enviando: {msg}")
    client_socket.sendall((msg + "\n").encode('utf-8'))

    respuesta = client_socket.recv(1024).decode('utf-8').replace("\n", "")
    client_socket.close()

    print(f"Respuesta de SIM: {respuesta}")
    return respuesta
