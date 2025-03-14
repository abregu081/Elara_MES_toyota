# Marzo. Abregu Tomas para proyecto Harman/Toyota. Mirgor
#
# Version 1.0 (adaptada):
#   - Primera implementación de registro en SIM y hermanado de equipos,
#   - Incluye flujo de BREQ/BCNF para sn1 y sn2,
#   - Luego BCMP/BACK para homologar (id=sn2, pid=sn1).

import socket
import datetime
import sys
import time
from collections import deque
import os

def printand(data):
    """
    Imprime información de seguimiento si tracelog está activo en setting.cfg
    """
    if(setting.get('tracelog') == "1"):
        print()
        print(str(data))

def read_setting(file):
    """
    Lee un archivo de configuración con formato clave=valor
    Ignora líneas que empiecen con # o que no contengan '='
    Retorna un diccionario con los parámetros
    """
    setting = {}
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): 
                continue
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            setting[key.strip()] = value.strip()
    return setting

def send_message(ip, port, msg):
    """
    Envía un mensaje (string) al servidor SIM usando socket TCP.
    Agrega un salto de línea al final.
    Retorna la respuesta recibida como string.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(int(setting['timeout_mes']))
    client_socket.connect((ip, int(port)))

    print(f"Enviando: {msg}")
    client_socket.sendall((msg + "\n").encode('utf-8'))

    respuesta = client_socket.recv(1024).decode('utf-8').replace("\n", "")
    client_socket.close()

    print(f"Respuesta de SIM: {respuesta}")
    return respuesta

def check_breq_response(respuesta, sn):
    """
    Verifica que la respuesta a un BREQ sea BCNF|id=<sn>|status=PASS.
    Retorna True si es PASS, False de lo contrario.
    """
    # Se espera algo como: BCNF|id=GI000286280-0K090020705F0008|status=PASS
    if respuesta.startswith("BCNF"):
        partes = respuesta.split('|')
        # partes[0] = "BCNF"
        # partes[1] = "id=GI000286280-0K090020705F0008"
        # partes[2] = "status=PASS" (o FAIL)

        if len(partes) < 3:
            print("Respuesta BREQ incompleta:", partes)
            return False

        # Verificar que id coincida y status sea PASS
        id_str = partes[1]  # "id=GI000286280-0K090020705F0008"
        status_str = partes[2]  # "status=PASS" o "status=FAIL"

        if f"id={sn}" in id_str and "status=PASS" in status_str:
            print(f"BREQ para {sn}: PASS")
            return True
        else:
            print(f"BREQ para {sn}: FAIL o ID no coincide")
            return False
    else:
        print("Respuesta desconocida para BREQ:", respuesta)
        return False

def check_bcmp_response(respuesta, sn1, sn2):
    """
    Verifica que la respuesta a un BCMP sea BACK|id=<sn1>|status=PASS
    considerando que se envió (id=sn2, pid=sn1).
    Retorna True si es PASS, False de lo contrario.
    """
    # Se espera algo como: BACK|id=GI000286280-0K090020705F0008|status=PASS
    if respuesta.startswith("BACK"):
        partes = respuesta.split('|')
        # partes[0] = "BACK"
        # partes[1] = "id=GI000286280-0K090020705F0008"
        # partes[2] = "status=PASS"

        if len(partes) < 3:
            print("Respuesta BCMP incompleta:", partes)
            return False

        id_str = partes[1]      # "id=<pid>" (que es sn1)
        status_str = partes[2]  # "status=PASS"

        # Verificar que la respuesta contenga el pid correcto (sn1) y sea PASS
        if f"id={sn1}" in id_str and "status=PASS" in status_str:
            print(f"BCMP: Hermanación OK -> sn2={sn2} con pid={sn1}")
            return True
        else:
            print("BCMP: Respuesta FAIL o ID no coincide con sn1")
            return False
    else:
        print("Respuesta con prefijo distinto de BACK. No se procesa:", respuesta)
        return False

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

current_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
setting = read_setting(os.path.join(current_directory, 'setting.cfg'))
printand(["Setting: ", setting])

# Cola circular para evitar reenvíos duplicados (opcional, si lo necesitas)
log_circular = deque(maxlen=500)

while True:
    # 1) Pedir o escanear  Serial Number 1
    sn1 = input("\nEscanear primer Serial Number (sn1): ")

    # 2) Enviar BREQ con sn1
    breq_msg_sn1 = f"BREQ|process={setting['process']}|station={setting['station']}|id={sn1}"
    respuesta_sn1 = send_message(setting['ip'], setting['port'], breq_msg_sn1)
    if not check_breq_response(respuesta_sn1, sn1):
        print("No se puede continuar: Primer SN (sn1) no validado con PASS.")
        continue  # o break si deseas terminar
    
    # 3) Pedir o escanear el segundo Serial Number
    sn2 = input("Escanear segundo Serial Number (sn2): ")

    # 4) Enviar BREQ con sn2
    breq_msg_sn2 = f"BREQ|process={setting['process']}|station={setting['station']}|id={sn2}"
    respuesta_sn2 = send_message(setting['ip'], setting['port'], breq_msg_sn2)
    if not check_breq_response(respuesta_sn2, sn2):
        print("No se puede continuar: Segundo SN (sn2) no validado con PASS.")
        continue  # o break si deseas terminar

    # 4) Enviar BCMP con id=sn2 y pid=sn1
    bcmp_msg = (
        "BCMP|"
        f"process={setting['process']}|"
        f"station={setting['station']}|"
        f"id={sn2}|"
        f"pid={sn1}|"
        "status=PASS"
    )
    respuesta_bcmp = send_message(setting['ip'], setting['port'], bcmp_msg)
    if check_bcmp_response(respuesta_bcmp, sn1, sn2):
        print("Hermanación completa. ¡Proceso finalizado con éxito!")
    else:
        print("Falló la hermanación final con BCMP.")

    # 5) Espera (periodo) antes de la siguiente iteración, si corresponde
    periodo = int(setting.get("periodo", 10))
    print(f"Esperando {periodo} segundos antes de la siguiente operación...")
    time.sleep(periodo)
