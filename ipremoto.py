import subprocess
import tkinter as tk
from tkinter import messagebox

def block_ping(ip_address):
    command = f'netsh advFirewall firewall add rule name="Regla Solvetic PING IPv6" protocol=icmpv4:8,any dir=in action=block remoteip={ip_address}'
    execute_command(command)

def allow_ping(ip_address):
    command = f'netsh advFirewall firewall add rule name="Regla Solvetic PING IPv6" protocol=icmpv4:8,any dir=in action=allow remoteip={ip_address}'
    execute_command(command)

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        messagebox.showinfo("Success", "Command executed successfully.")
    except subprocess.CalledProcessError as e:
        error_message = f"Error executing command:\n{e}\n\nCommand output:\n{e.output}\n\nCopie este mensaje para referencia."
        messagebox.showerror("Error", error_message)
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error:\n{e}")

def on_block_button_click():
    ip_address = ip_entry.get()
    if ip_address:
        block_ping(ip_address)
    else:
        messagebox.showerror("Error", "Please enter an IP address.")

def on_allow_button_click():
    ip_address = ip_entry.get()
    if ip_address:
        allow_ping(ip_address)
    else:
        messagebox.showerror("Error", "Please enter an IP address.")

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Control de Ping")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Etiqueta y entrada para la dirección IP
ip_label = tk.Label(frame, text="Dirección IP:")
ip_label.pack()

ip_entry = tk.Entry(frame, width=30)
ip_entry.pack(pady=10)

block_button = tk.Button(frame, text="Bloquear Ping", command=on_block_button_click)
block_button.pack(pady=10)

allow_button = tk.Button(frame, text="Permitir Ping", command=on_allow_button_click)
allow_button.pack(pady=10)

quit_button = tk.Button(frame, text="Salir", command=root.destroy)
quit_button.pack(pady=10)

root.mainloop()
