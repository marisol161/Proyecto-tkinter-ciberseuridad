import socket
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import PhotoImage

# Función para enviar comando al cliente
def enviar_comando(ip, comando):
    try:
        # Crear socket del cliente
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, 50020))
        
        # Enviar comando al cliente
        client_socket.send(comando.encode())
        
        # Recibir respuesta del cliente
        respuesta = client_socket.recv(1024).decode()
        messagebox.showinfo("Respuesta del cliente", respuesta)
        
        # Cerrar conexión
        client_socket.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar al cliente: {e}")

# Crear ventana principal
root = tk.Tk()
root.title("Control de Apagado")

# Cargar el icono de la ventana
try:
    image_icon = PhotoImage(file="img/apagar.png")
    root.iconphoto(False, image_icon)
except Exception as e:
    print(f"Error al cargar el icono: {e}")

# Cargar imágenes para los botones
try:
    img_portatil1 = ImageTk.PhotoImage(Image.open("img/portatil1.png"))
    img_portatil2 = ImageTk.PhotoImage(Image.open("img/portatil2.png"))
except Exception as e:
    messagebox.showerror("Error", f"No se pudieron cargar las imágenes: {e}")
    root.destroy()
    exit()

# Crear frame para organizar botones y etiquetas
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

# Crear botones con imágenes
btn_portatil1 = tk.Button(frame1, image=img_portatil1, command=lambda: enviar_comando('172.168.2.163', 'apagar'))
btn_portatil2 = tk.Button(frame2, image=img_portatil2, command=lambda: enviar_comando('172.168.2.163', 'apagar'))

# Crear etiquetas
label_portatil1 = tk.Label(frame1, text="HP")
label_portatil2 = tk.Label(frame2, text="HP")

# Colocar botones y etiquetas en los frames
btn_portatil1.pack(pady=5)
label_portatil1.pack()
btn_portatil2.pack(pady=5)
label_portatil2.pack()

# Colocar los frames en la ventana
frame1.pack(side=tk.LEFT, padx=10, pady=10)
frame2.pack(side=tk.RIGHT, padx=10, pady=10)

# Iniciar bucle de la aplicación
root.mainloop()
