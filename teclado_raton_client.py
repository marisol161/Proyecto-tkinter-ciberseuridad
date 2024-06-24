import tkinter as tk
import socket
from PIL import Image, ImageTk  # Asegúrate de tener Pillow instalado

# Configuración del cliente
SERVER_HOST = '172.168.0.199'
SERVER_PORT = 54001

# Función para enviar comando al servidor
def send_command(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            client_socket.sendall(command.encode())
    except Exception as e:
        print(f"Error al enviar comando: {e}")

# Crear la ventana principal
root = tk.Tk()
root.title('Control de Dispositivos de Entrada')

# Colocar el icono de la ventana
root.iconbitmap('img/candado.png')

# Función para deshabilitar dispositivos
def disable_devices():
    send_command('disable_devices')

# Función para habilitar dispositivos
def enable_devices():
    send_command('enable_devices')

# Cargar imágenes
img_disable = Image.open('img/bloqueo1.png')
img_disable = ImageTk.PhotoImage(img_disable)

img_enable = Image.open('img/desbloqueo1.png')
img_enable = ImageTk.PhotoImage(img_enable)

# Crear botones con imágenes
btn_disable = tk.Button(root, image=img_disable, command=disable_devices)
btn_disable.grid(row=0, column=0, padx=20, pady=10)

btn_enable = tk.Button(root, image=img_enable, command=enable_devices)
btn_enable.grid(row=0, column=1, padx=20, pady=10)

# Crear etiquetas para los botones
lbl_disable = tk.Label(root, text='Deshabilitar Teclado y Ratón')
lbl_disable.grid(row=1, column=0, pady=5)

lbl_enable = tk.Label(root, text='Habilitar Teclado y Ratón')
lbl_enable.grid(row=1, column=1, pady=5)

# Ejecutar la ventana
root.mainloop()
