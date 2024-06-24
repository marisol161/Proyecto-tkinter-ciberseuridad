import cv2
import socket
import struct
import numpy as np
from PIL import ImageGrab

# Configuración del servidor
SERVER_IP = '172.168.2.163'
SERVER_PORT = 12345

def main():
    # Crear socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    connection = client_socket.makefile('wb')

    try:
        while True:
            # Capturar la pantalla
            img = ImageGrab.grab()
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

            # Codificar la imagen
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = frame.tobytes()

            # Enviar tamaño de la imagen y la imagen
            client_socket.sendall(struct.pack(">L", len(data)) + data)
    finally:
        client_socket.close()

if __name__ == '__main__':
    main()