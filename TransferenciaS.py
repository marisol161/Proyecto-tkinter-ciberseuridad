from tkinter import *
import socket
from tkinter import filedialog
from tkinter import messagebox
import os

root = Tk()
root.title("Transferencia de archivos")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

def Send():
    window = Toplevel(root)
    window.title("Enviar")
    window.geometry('450x560+500+200')
    window.configure(bg="#f4fdfe")
    window.resizable(False, False)

    def select_file():
        global filename
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                              title='Selecciona un archivo',
                                              filetype=(('file_type', '*.txt'), ('all files', '*.*')))
    
    def sender():
        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print(f"Host: {host}")
        print('Esperando conexión...')
        conn, addr = s.accept()
        print(f"Conectado a: {addr}")

        try:
            with open(filename, 'rb') as file:
                file_size = os.path.getsize(filename)
                file_name = os.path.basename(filename)
                conn.send(f"{file_name}:{file_size}".encode())  # Enviar nombre y tamaño del archivo
                conn.recv(1024)  # Esperar confirmación de recepción

                while True:
                    file_data = file.read(1024)
                    if not file_data:
                        break
                    conn.send(file_data)
            print("Archivo enviado satisfactoriamente.")
        except Exception as e:
            print(f"Error durante el envío: {e}")
        finally:
            conn.close()
            s.close()

    # Icon
    image_icon1 = PhotoImage(file="img/enviar.png")
    window.iconphoto(False, image_icon1)

    Sbackground = PhotoImage(file="img/fondo1.png")
    Label(window, image=Sbackground).place(x=-2, y=0)

    Mbackground = PhotoImage(file="img/id.png")
    Label(window, image=Mbackground, bg='#f4fdfe').place(x=100, y=260)

    host = socket.gethostname()
    Label(window, text=f'ID: {host}', bg='white', fg='black').place(x=165, y=310)

    Button(window, text="+ Archivo", width=10, height=1, font='arial 14 bold', bg='#fff', fg='#000', command=select_file).place(x=160, y=150)
    Button(window, text="Enviar", width=8, height=1, font='arial 14 bold', bg='#000', fg='#fff', command=sender).place(x=300, y=150)

    window.mainloop()

# ------------------------------------------------------------------------------------------------------------
#                                     VENTANA DE RECEPCIÓN DE ARCHIVO
# -------------------------------------------------------------------------------------------------------------

def Receive():
    main = Toplevel(root)
    main.title("Recibir")
    main.geometry('450x560+500+200')
    main.configure(bg="#f4fdfe")
    main.resizable(False, False)

    def receiver():
        ID = SenderID.get()

        s = socket.socket()
        port = 8080
        try:
            s.connect((ID, port))
            file_info = s.recv(1024).decode()  # Recibir nombre y tamaño del archivo
            file_name, file_size = file_info.split(':')
            file_size = int(file_size)
            s.send(b"INFO RECEIVED")  # Enviar confirmación de recepción de la información

            received_data = 0
            with open(file_name, 'wb') as file:
                while received_data < file_size:
                    file_data = s.recv(1024)
                    if not file_data:
                        break
                    file.write(file_data)
                    received_data += len(file_data)
            print("El archivo ha sido recibido satisfactoriamente")
        except ConnectionRefusedError:
            print("No se puede establecer una conexión, el equipo de destino denegó la conexión")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            s.close()

    # Icono de la ventana de recibir
    image_icon1 = PhotoImage(file="img/guardar.png")
    main.iconphoto(False, image_icon1)

    # Fondo superior de la ventana de recibir
    Hbackground = PhotoImage(file="img/receiver.png")
    Label(main, image=Hbackground).place(x=-2, y=0)

    # Imagen de perfil
    logo = PhotoImage(file='img/perfil.png')
    Label(main, image=logo, bg="#f4fdfe").place(x=10, y=200)

    Label(main, text="Recibir", font=('arial', 20), bg="#f4fdfe").place(x=100, y=200)

    Label(main, text="Introduce el ID de envío", font=('arial', 10, 'bold'), bg="#f4fdfe").place(x=20, y="310")
    SenderID = Entry(main, width=25, fg="black", border=2, bg='white', font=('arial', 15))
    SenderID.place(x=20, y=340)
    SenderID.focus()
    
    imageicon = PhotoImage(file='img/recibido.png')
    rr = Button(main, text="Recibir", compound=LEFT, image=imageicon, width=130, bg="#D9D9D9", font="arial 14 bold", command=receiver)
    rr.place(x=20, y=470)

    main.mainloop()

# ------------------------------------------------------------------------------------------------------------
#                                           VENTANA PRINCIPAL
# -------------------------------------------------------------------------------------------------------------

# Icono de la ventana principal
image_icon = PhotoImage(file="img/compartirIcono.png")
root.iconphoto(False, image_icon)

# Label para el titulo de proyecto
Label(root, text="File Transfer", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=20, y=30)
Frame(root, width=400, height=2, bg="#f3f5f6").place(x=25, y=80)

# ------------------------------BOTON DE ENVIAR----------------------------------------------------------

# Icono y programación del botón de enviar en la ventana principal
send_image = PhotoImage(file="img/enviar.png")
send = Button(root, image=send_image, bg="#f4fdfe", bd=0, command=Send)
send.place(x=50, y=100)

# ------------------------------BOTON DE RECIBIR-------------------------------------------------------
# Icono y programación del botón de recibir en la ventana principal
receive_image = PhotoImage(file="img/descargable.png")
receive = Button(root, image=receive_image, bg="#f4fdfe", bd=0, command=Receive)
receive.place(x=300, y=100)

# ------------------------------ETIQUETAS DE ENVIAR/RECIBIR----------------------------------------------

# Label de cada uno de los botones de Enviar o Recibir
Label(root, text="Enviar", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=50, y=180)
Label(root, text="Recibir", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=300, y=180)

# ------------------------IMAGEN DE FONDO INFERIOR PANTALLA PRINCIPAL------------------------------------

# Imagen de fondo inferior en la ventana principal
background = PhotoImage(file="img/archivos.png")
Label(root, image=background).place(x=-2, y=323)

root.mainloop()
