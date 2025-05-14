import csv
import os
import sys
from datetime import datetime


def guardar_log_csv(sn1, resultado, envio_sim, devolucion_sim):
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    carpeta_base = os.path.join("logs", resultado.upper())
    os.makedirs(carpeta_base, exist_ok=True)
    archivo_nombre = f"{sn1}_{fecha_hora}.csv"
    ruta_completa = os.path.join(carpeta_base, archivo_nombre)

    # Guardar CSV con campos
    with open(ruta_completa, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SN1", "Resultado", "Fecha", "Hora", "Envio a SIM", "Devolucion de SIM"])
        writer.writerow([
            sn1,
            resultado,
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M:%S"),
            envio_sim,
            devolucion_sim
        ])
