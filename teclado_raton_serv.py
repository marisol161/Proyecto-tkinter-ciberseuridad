import socket
import ctypes
import subprocess

# Configuración del servidor
SERVER_HOST = '0.0.0.0'  # Escuchar en todas las interfaces disponibles
SERVER_PORT = 54001

# Ruta de los scripts AHK
BLOCK_MOUSE_SCRIPT = r'C:\Users\Administrador\OneDrive\Escritorio\SEMESTRE\OCTAVO SEMESTRE\CIBERSEGURIDAD\proyecto-tkinter\lock_mouse.ahk'
UNBLOCK_MOUSE_SCRIPT = r'C:\Users\Administrador\OneDrive\Escritorio\SEMESTRE\OCTAVO SEMESTRE\CIBERSEGURIDAD\proyecto-tkinter\unblock_mouse.ahk'

# Función para deshabilitar el teclado y ratón
def disable_devices():
    try:
        print("[*] Bloqueando entradas de teclado y ratón")
        # Bloquear todas las entradas de teclado y ratón
        ctypes.windll.user32.BlockInput(True)
        # Ejecutar script AHK para bloquear el ratón
        result = subprocess.run([r"C:\Program Files\AutoHotkey\v1.1.37.02\AutoHotkeyU64.exe", BLOCK_MOUSE_SCRIPT], capture_output=True, text=True)
        if result.returncode == 0:
            print("[*] Teclado y ratón deshabilitados")
        else:
            print(f"Error al ejecutar script AHK para bloquear el ratón: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar script AHK para bloquear el ratón: {e}")
    except Exception as e:
        print(f"Error al deshabilitar dispositivos: {e}")

# Función para habilitar el teclado y ratón
def enable_devices():
    try:
        # Desbloquear todas las entradas de teclado y ratón
        print("[*] Desbloqueando entradas de teclado y ratón")
        ctypes.windll.user32.BlockInput(False)
        # Ejecutar script AHK para desbloquear el ratón
        result = subprocess.run([r"C:\Program Files\AutoHotkey\v1.1.37.02\AutoHotkeyU64.exe", UNBLOCK_MOUSE_SCRIPT], capture_output=True, text=True)
        if result.returncode == 0:
            print("[*] Teclado y ratón habilitados")
        else:
            print(f"Error al ejecutar script AHK para desbloquear el ratón: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar script AHK para desbloquear el ratón: {e}")
    except Exception as e:
        print(f"Error al habilitar dispositivos: {e}")

# Función principal del servidor
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(1)
        print(f"[*] Escuchando en {SERVER_HOST}:{SERVER_PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"[*] Conexión establecida desde: {client_address}")

            try:
                while True:
                    command = client_socket.recv(1024).decode().strip()
                    if not command:
                        break
                    print(f"[*] Comando recibido: {command}")

                    if command == 'disable_devices':
                        disable_devices()
                    elif command == 'enable_devices':
                        enable_devices()
                    else:
                        print(f"[*] Comando no reconocido: {command}")

            finally:
                client_socket.close()

if __name__ == "__main__":
    main()