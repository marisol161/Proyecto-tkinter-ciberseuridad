import socket
import threading
import tkinter as tk
from PIL import Image, ImageTk

class Application():
    def __init__(self):
        self.clients = []
        self.bloqueadas = []  # Lista para almacenar las URL e IP bloqueadas
        self.window = tk.Tk()
        self.window.geometry("400x180")
        self.window.title("Bloqueador de páginas web")
        self.window.resizable(width=False, height=False)
        self.window.iconphoto(False, tk.PhotoImage(file='img/web.png'))

        self.createLabelEntryFrame()
        self.createButtonFrame()
        self.loadIcons()
        self.createButtons()

    def createLabelEntryFrame(self):
        self.labelEntryFrame = tk.Frame(self.window)
        self.labelEntryFrame.pack(pady=5)
        
        self.url_label = tk.Label(self.labelEntryFrame, text="Ingresa URL:")
        self.url_label.pack(side=tk.LEFT, padx=5)
        
        self.url_entry = tk.Entry(self.labelEntryFrame, width=20)
        self.url_entry.pack(side=tk.LEFT, padx=5)

        self.ip_label = tk.Label(self.labelEntryFrame, text="Ingresa IP:")
        self.ip_label.pack(side=tk.LEFT, padx=5)
        
        self.ip_entry = tk.Entry(self.labelEntryFrame, width=15)
        self.ip_entry.pack(side=tk.LEFT)

    def createButtonFrame(self):
        self.buttonFrame = tk.Frame(self.window)
        self.buttonFrame.pack(pady=5)

    def loadIcons(self):
        self.addIcon = ImageTk.PhotoImage(Image.open("img/enlace.png").resize((50, 50), Image.Resampling.LANCZOS))
        self.removeIcon = ImageTk.PhotoImage(Image.open("img/borrar.png").resize((50, 50), Image.Resampling.LANCZOS))
        self.listIcon = ImageTk.PhotoImage(Image.open("img/lista.png").resize((50, 50), Image.Resampling.LANCZOS))

    def createButtons(self):
        self.addButton = tk.Button(self.buttonFrame, image=self.addIcon, command=self.agregar_url)
        self.addButton.grid(row=0, column=0, padx=5)
        self.addLabel = tk.Label(self.buttonFrame, text="Añadir")
        self.addLabel.grid(row=1, column=0)

        self.removeButton = tk.Button(self.buttonFrame, image=self.removeIcon, command=self.eliminar_url)
        self.removeButton.grid(row=0, column=1, padx=5)
        self.removeLabel = tk.Label(self.buttonFrame, text="Eliminar")
        self.removeLabel.grid(row=1, column=1)

        self.listButton = tk.Button(self.buttonFrame, image=self.listIcon, command=self.listar_url)
        self.listButton.grid(row=0, column=2, padx=5)
        self.listLabel = tk.Label(self.buttonFrame, text="Urls bloqueadas")
        self.listLabel.grid(row=1, column=2)

    def agregar_url(self):
        url = self.url_entry.get()
        ip = self.ip_entry.get()
        if url and ip:
            full_url = f"www.{url}.com"
            self.send_command_to_clients(f"add,{ip},{full_url}")
            self.bloqueadas.append({'ip': ip, 'url': full_url})  # Añadir a la lista
            self.url_entry.delete(0, tk.END)
            self.ip_entry.delete(0, tk.END)

    def eliminar_url(self):
        url = self.url_entry.get()
        ip = self.ip_entry.get()
        if url and ip:
            full_url = f"www.{url}.com"
            self.send_command_to_clients(f"remove,{ip},{full_url}")
            self.bloqueadas = [entry for entry in self.bloqueadas if not (entry['ip'] == ip and entry['url'] == full_url)]  # Eliminar de la lista
            self.url_entry.delete(0, tk.END)
            self.ip_entry.delete(0, tk.END)

    def listar_url(self):
        new_window = tk.Tk()
        new_window.geometry("400x400")
        new_window.title("Páginas Bloqueadas")
        new_window.resizable(width=False, height=False)

        listbox = tk.Listbox(new_window, width=50, height=20)
        listbox.pack(pady=10)

        for entry in self.bloqueadas:
            listbox.insert(tk.END, f"{entry['ip']}  {entry['url']}")

        new_window.mainloop()

    def send_command_to_clients(self, command):
        for client in self.clients:
            try:
                client.sendall(command.encode())
            except:
                self.clients.remove(client)

def handle_client_connection(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
        except ConnectionResetError:
            break
    client_socket.close()

def start_server(app):
    SERVER_IP = '0.0.0.0'
    SERVER_PORT = 12346  # Cambiado a otro puerto
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen()
        print("Servidor escuchando...")
        while True:
            client_socket, addr = s.accept()
            print(f"Conexión establecida con {addr}")
            app.clients.append(client_socket)
            client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    app = Application()
    server_thread = threading.Thread(target=start_server, args=(app,))
    server_thread.start()
    app.window.mainloop()
