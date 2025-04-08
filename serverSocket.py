import socket
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

settings_path = os.path.join(current_directory, 'settings.cfg')

def read_setting(file):
    setting = {}
    with open(file, 'r') as f:
        for line in f:
            if(not line or '=' not in line): continue
            if(line[0]=="#"): continue
            key, value = line.split('=', 1)
            if key and value:
              setting[key.strip()] = value.strip()
    return setting

def start_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, int(port)))
    server_socket.listen(1)
    print(f"Esperando conexión en {ip}:{port}...")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Conexión establecida con {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mensaje = data.decode('utf-8')
            print(f"Mensaje recibido: {mensaje}")

            # Enviar una respuesta al cliente
            respuesta = f"Mensaje '{mensaje}' recibido correctamente"
            conn.sendall(respuesta.encode('utf-8'))

if __name__ == "__main__":
    setting = read_setting(os.path.join(current_directory, 'setting.cfg'))
    start_server(setting['ip'], setting['port'])