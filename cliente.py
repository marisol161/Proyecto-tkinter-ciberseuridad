import socket
import struct
import zlib
import cv2
import numpy as np
import time
from PIL import Image
import io

def receive_data(client_socket):
    data = b""
    payload_size = struct.calcsize("L")
    
    while len(data) < payload_size:
        packet = client_socket.recv(4096)
        if not packet:
            raise ConnectionError("Conexión cerrada por el servidor.")
        data += packet
    
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0]
    
    while len(data) < msg_size:
        packet = client_socket.recv(4096)
        if not packet:
            raise ConnectionError("Conexión cerrada por el servidor.")
        data += packet
    
    frame_data = data[:msg_size]
    return frame_data

def client():
    host = '172.168.2.47'
    port = 55555
    
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            print('Conectado al servidor')

            while True:
                try:
                    frame_data = receive_data(client_socket)
                    
                    decompressed_data = zlib.decompress(frame_data)
                    image = Image.open(io.BytesIO(decompressed_data))
                    frame = np.array(image)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    cv2.imshow('Remote Desktop', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                except (ConnectionResetError, BrokenPipeError):
                    print("Error de comunicación, intentando reconectar...")
                    break
                except Exception as e:
                    print(f'Error al recibir datos: {e}')
                    break
        
        except Exception as e:
            print(f'Error en la conexión: {e}')
        
        finally:
            cv2.destroyAllWindows()
            client_socket.close()
            print('Desconectado del servidor, intentando reconectar en 5 segundos...')
            time.sleep(5)

if __name__ == '__main__':
    client()