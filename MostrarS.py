import socket
import cv2
import numpy as np
import pyautogui
import tkinter as tk
from tkinter import messagebox
import threading

class ScreenShareServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.running = False
        self.lock = threading.Lock()

    def start_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print(f'Servidor escuchando en {self.host}:{self.port}')

            self.client_socket, client_address = self.server_socket.accept()
            print(f'Cliente conectado desde {client_address}')
            self.running = True

            self.send_screenshots()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.stop_server()

    def send_screenshots(self):
        try:
            while self.running:
                # Capturar la pantalla
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Codificar la imagen
                _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                data = buffer.tobytes()

                # Enviar el tamaño del frame
                size = len(data)
                self.client_socket.sendall(size.to_bytes(4, byteorder='big'))
                
                # Enviar el frame
                self.client_socket.sendall(data)
            
            # Enviar una señal de terminación
            self.client_socket.sendall((0).to_bytes(4, byteorder='big'))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.stop_server()

    def stop_server(self):
        with self.lock:
            self.running = False
            if self.client_socket:
                self.client_socket.close()
            if self.server_socket:
                self.server_socket.close()
            print('Conexión cerrada')

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Share Server")
        self.root.geometry("200x350")

        try:
            # Cargar las imágenes
            self.start_image = tk.PhotoImage(file="img/vivo.png")
            self.stop_image = tk.PhotoImage(file="img/stopp.png")
            self.icon_image = tk.PhotoImage(file="img/transmision.png")

            # Establecer el icono de la ventana
            self.root.iconphoto(False, self.icon_image)

            # Crear los botones con las imágenes
            self.start_button = tk.Button(root, image=self.start_image, command=self.start_server, borderwidth=0)
            self.start_button.pack(pady=20)

            self.stop_button = tk.Button(root, image=self.stop_image, command=self.stop_server, state=tk.DISABLED, borderwidth=0)
            self.stop_button.pack(pady=20)
        except Exception as e:
            print(f"Error al cargar las imágenes: {e}")

        self.server = ScreenShareServer('172.168.0.199', 50016)

    def start_server(self):
        print("Starting server...")
        self.server_thread = threading.Thread(target=self.server.start_server)
        self.server_thread.start()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        print("Server started.")

    def stop_server(self):
        print("Stopping server...")
        self.server.stop_server()
        self.server_thread.join()  # Wait for the server thread to finish
        print("Server stopped.")
        self.root.quit()  # Close the Tkinter window
        self.root.destroy()  # Ensure the Tkinter window is properly destroyed
        print("Window closed.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
