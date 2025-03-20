# Marzo. Abregu Tomas para proyecto Harman/Toyota. Mirgor

# Version 1.0 (adaptada):
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

def load_settings():
    global setting
    setting.clear()  # Limpia la configuración anterior
    
    try:
        with open("setting.cfg", "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                setting[key] = value

        print("⚡ Configuración recargada:", setting)  # ✅ Verifica que se cargan los valores

    except Exception as e:
        print(f"⚠️ Error al cargar configuración: {e}")

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
    timeout = int(setting.get('timeout_mes', 10))
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(timeout)
    client_socket.connect((ip, int(port)))

    print(f"Enviando: {msg}")
    client_socket.sendall((msg + "\n").encode('utf-8'))

    respuesta = client_socket.recv(1024).decode('utf-8').replace("\n", "")
    client_socket.close()

    print(f"Respuesta de SIM: {respuesta}")
    return respuesta

def check_breq_response(respuesta, sn):
    """
    Verifica que la respuesta a un BREQ sea:
      BCNF|id=<sn>|status=PASS
    Retorna True si es PASS, False de lo contrario.
    """
    if respuesta.startswith("BCNF"):
        partes = respuesta.split('|')
        if len(partes) < 3:
            print("Respuesta BREQ incompleta:", partes)
            return False
        # partes[1] = "id=GI000286280-0K090020705F0008"
        # partes[2] = "status=PASS"

        if f"id={sn}" in partes[1] and "status=PASS" in partes[2]:
            print(f"BREQ para {sn}: PASS")
            return True
        else:
            print(f"BREQ para {sn}: FAIL (ID o STATUS no coinciden)")
            return False
    else:
        print("Respuesta desconocida para BREQ:", respuesta)
        return False

def check_bcmp_response(respuesta, sn1, sn2):
    """
    Verifica que la respuesta a un BCMP sea:
      BACK|id=<sn1>|status=PASS
    asumiendo que se envió BCMP con (id=sn2, pid=sn1).
    Retorna True si es PASS, False de lo contrario.
    """
    if respuesta.startswith("BACK"):
        partes = respuesta.split('|')
        if len(partes) < 3:
            print("Respuesta BCMP incompleta:", partes)
            return False
        # partes[1] = "id=GI000286280-0K090020705F0008"
        # partes[2] = "status=PASS"

        if f"id={sn1}" in partes[1] and "status=PASS" in partes[2]:
            print(f"BCMP: Hermanación OK -> sn2={sn2} con pid={sn1}")
            return True
        else:
            print("BCMP: Respuesta FAIL o ID no coincide con sn1")
            return False
    else:
        print("Respuesta con prefijo distinto de BACK. No se procesa:", respuesta)
        return False
    
def check_bcmp_response2(respuesta, sn1):
    ...



# ------------------------------------------------------------
# (Opcional) Mover la antigua lógica de input a una función
# ------------------------------------------------------------
def run_terminal_mode():
    """
    Modo interactivo por consola:
     1) Escanea sn1 y sn2
     2) BREQ->BCNF
     3) BREQ->BCNF
     4) BCMP->BACK
     5) Repite con un delay
    """
    load_settings()  # carga global setting
    log_circular = deque(maxlen=500)

    while True:
        sn1 = input("\nEscanear primer Serial Number (sn1): ")
        sn2 = input("Escanear segundo Serial Number (sn2): ")

        # BREQ 1
        breq_sn1 = f"BREQ|process={setting['process']}|station={setting['station']}|id={sn1}"
        resp_sn1 = send_message(setting['ip'], setting['port'], breq_sn1)
        if not check_breq_response(resp_sn1, sn1):
            print("No se puede continuar: sn1 no validado con PASS.")
            continue

        # BREQ 2
        breq_sn2 = f"BREQ|process={setting['process']}|station={setting['station']}|id={sn2}"
        resp_sn2 = send_message(setting['ip'], setting['port'], breq_sn2)
        if not check_breq_response(resp_sn2, sn2):
            print("No se puede continuar: sn2 no validado con PASS.")
            continue

        # BCMP
        bcmp_msg = f"BCMP|process={setting['process']}|station={setting['station']}|id={sn2}|pid={sn1}|status=PASS"
        resp_bcmp = send_message(setting['ip'], setting['port'], bcmp_msg)
        if check_bcmp_response(resp_bcmp, sn1, sn2):
            print("Hermanación completa. ¡Proceso finalizado con éxito!")
        else:
            print("Falló la hermanación final con BCMP.")

        periodo = int(setting.get("periodo", 10))
        print(f"Esperando {periodo} segundos antes de la siguiente operación...")
        time.sleep(periodo)


if __name__ == "__main__":
    # run_terminal_mode()
    pass
