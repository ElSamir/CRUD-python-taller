import tkinter as tk
from tkinter import messagebox, simpledialog
import os

ventanaUsuario = None
# Agregar una variable global para almacenar los clientes registrados
clientes_registrados = set()


# Función para registrar un nuevo cliente
def registrar_cliente():
    nuevo_cliente_id = entry_cliente_id.get()
    nuevo_nombre = entry_nombre_cliente.get()
    nuevo_apellido_paterno = entry_apellido_paterno_cliente.get()
    nuevo_apellido_materno = entry_apellido_materno_cliente.get()

    # Validar que el Cliente ID no esté repetido
    if nuevo_cliente_id in clientes_registrados:
        messagebox.showerror("Error", "Cliente ID ya existe")
    else:
        with open("clientes.txt", "a") as file:
            file.write(
                f"{nuevo_cliente_id},{nuevo_nombre},{nuevo_apellido_paterno},{nuevo_apellido_materno}\n")

        clientes_registrados.add(nuevo_cliente_id)

        messagebox.showinfo("Éxito", "Cliente registrado con éxito")
        ventanaClientes.destroy()

# Función para abrir la ventana de registro de clientes


def abrir_ventana_clientes():
    global ventanaClientes, entry_cliente_id, entry_nombre_cliente, entry_apellido_paterno_cliente, entry_apellido_materno_cliente

    ventanaClientes = tk.Toplevel()
    ventanaClientes.geometry("600x300")
    ventanaClientes.title("Registrar Cliente")

    tk.Label(ventanaClientes, text="Cliente ID:").place(x=10, y=10)
    entry_cliente_id = tk.Entry(ventanaClientes)
    entry_cliente_id.place(x=150, y=10)

    tk.Label(ventanaClientes, text="Nombre:").place(x=10, y=40)
    entry_nombre_cliente = tk.Entry(ventanaClientes)
    entry_nombre_cliente.place(x=150, y=40)

    tk.Label(ventanaClientes, text="Apellido Paterno:").place(x=10, y=70)
    entry_apellido_paterno_cliente = tk.Entry(ventanaClientes)
    entry_apellido_paterno_cliente.place(x=150, y=70)

    tk.Label(ventanaClientes, text="Apellido Materno:").place(x=10, y=100)
    entry_apellido_materno_cliente = tk.Entry(ventanaClientes)
    entry_apellido_materno_cliente.place(x=150, y=100)

    # Selector para elegir la ID del usuario registrado
    tk.Label(ventanaClientes, text="Seleccionar Usuario ID:").place(x=10, y=130)
    combo_usuario_id = tk.StringVar()
    combo_usuario_id.set("")  # Valor inicial en blanco
    combo_usuario_id_menu = tk.OptionMenu(
        ventanaClientes, combo_usuario_id, *usuarios_registrados)
    combo_usuario_id_menu.place(x=200, y=130)

    btn_registrar_cliente = tk.Button(
        ventanaClientes, text="Registrar Cliente", command=registrar_cliente)
    btn_registrar_cliente.place(x=10, y=160)

# Función para registrar un nuevo usuario


def registrar_usuario():
    nuevo_id = entry_id.get()
    nuevo_nombre = entry_nombre.get()
    nuevo_apellido_paterno = entry_apellido_paterno.get()
    nuevo_apellido_materno = entry_apellido_materno.get()
    nuevo_telefono = entry_telefono.get()
    nuevo_username = entry_username.get()
    nuevo_password = entry_password.get()
    nuevo_direccion = entry_direccion.get()
    nuevo_perfil = combo_perfil.get()  # Obtener el perfil seleccionado

    # Validar que el ID y el UserName sean únicos
    if nuevo_id in usuarios_registrados or nuevo_username in usuarios_registrados:
        messagebox.showerror("Error", "ID o UserName ya existen")
    else:
        with open("usuarios.txt", "a") as file:
            file.write(f"{nuevo_id},{nuevo_nombre},{nuevo_apellido_paterno},{nuevo_apellido_materno},{nuevo_telefono},{nuevo_username},{nuevo_password},{nuevo_direccion},{nuevo_perfil}\n")

        usuarios_registrados.add(nuevo_id)
        usuarios_registrados.add(nuevo_username)

        messagebox.showinfo("Éxito", "Usuario registrado con éxito")
        ventanaUsuario.destroy()

# Función para buscar usuarios por nombre o ID


def abrir_ventana_registrar_usuario():
    global ventanaUsuario  # Declarar ventanaUsuario como global
    ventanaUsuario = tk.Toplevel()
    ventanaUsuario.geometry("600x500")
    ventanaUsuario.title("Registrar Usuario")


def buscar_usuarios():
    buscar_texto = entry_buscar.get().lower()
    usuarios_encontrados = []

    with open("usuarios.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                nombre_completo = f"{parts[1]} {parts[2]}"
                if buscar_texto in nombre_completo.lower() or buscar_texto == parts[0].lower():
                    # Ocultar la contraseña antes de agregar la línea
                    parts[6] = "********"
                    usuarios_encontrados.append(parts)  # Agregar toda la línea

    if usuarios_encontrados:
        mostrar_usuarios_encontrados(usuarios_encontrados)
    else:
        messagebox.showinfo("Usuarios Encontrados",
                            "Ningún usuario encontrado.")

# Función para mostrar los usuarios encontrados y seleccionar uno para editar


def mostrar_usuarios_encontrados(usuarios_encontrados):
    ventana_usuarios_encontrados = tk.Toplevel()
    ventana_usuarios_encontrados.geometry("400x300")
    ventana_usuarios_encontrados.title("Usuarios Encontrados")

    tk.Label(ventana_usuarios_encontrados, text="Usuarios encontrados:").pack()

    lista_usuarios = tk.Listbox(
        ventana_usuarios_encontrados, selectmode=tk.SINGLE)
    lista_usuarios.pack()

    for usuario in usuarios_encontrados:
        lista_usuarios.insert(
            tk.END, f"{usuario[1]} {usuario[2]}, ID: {usuario[0]}")

    def editar_seleccionado():
        seleccion = lista_usuarios.curselection()
        if seleccion:
            seleccion_index = seleccion[0]
            usuario_seleccionado = usuarios_encontrados[seleccion_index]
            cargar_datos_usuario(usuario_seleccionado)

    btn_editar = tk.Button(ventana_usuarios_encontrados,
                           text="Editar", command=editar_seleccionado)
    btn_editar.pack()

# Función para cargar los datos de un usuario en los campos de entrada


def cargar_datos_usuario(usuario):
    entry_id.delete(0, tk.END)
    entry_id.insert(0, usuario[0])
    entry_nombre.delete(0, tk.END)
    entry_nombre.insert(0, usuario[1])
    entry_apellido_paterno.delete(0, tk.END)
    entry_apellido_paterno.insert(0, usuario[2])
    entry_apellido_materno.delete(0, tk.END)
    entry_apellido_materno.insert(0, usuario[3])
    entry_telefono.delete(0, tk.END)
    entry_telefono.insert(0, usuario[4])
    entry_username.delete(0, tk.END)
    entry_username.insert(0, usuario[5])
    entry_password.delete(0, tk.END)
    entry_password.insert(0, usuario[6])
    entry_direccion.delete(0, tk.END)
    entry_direccion.insert(0, usuario[7])
    combo_perfil.set(usuario[8])

# Función para guardar los cambios de la edición


def guardar_cambios():
    id_usuario = entry_id.get()
    nuevo_nombre = entry_nombre.get()
    nuevo_apellido_paterno = entry_apellido_paterno.get()
    nuevo_apellido_materno = entry_apellido_materno.get()
    nuevo_telefono = entry_telefono.get()
    nuevo_username = entry_username.get()
    nuevo_password = entry_password.get()
    nuevo_direccion = entry_direccion.get()
    nuevo_perfil = combo_perfil.get()

    with open("usuarios.txt", "r") as file:
        lines = file.readlines()

    with open("usuarios.txt", "w") as file:
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 2 and parts[0] == id_usuario:
                line = f"{id_usuario},{nuevo_nombre},{nuevo_apellido_paterno},{nuevo_apellido_materno},{nuevo_telefono},{nuevo_username},{nuevo_password},{nuevo_direccion},{nuevo_perfil}\n"
            file.write(line)

        messagebox.showinfo("Éxito", "Cambios guardados exitosamente")

# Función para realizar el inicio de sesión


def iniciar_sesion():
    username = entry_username_login.get()
    password = entry_password_login.get()

    # Verificar si las credenciales son válidas
    with open("usuarios.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 6 and parts[5] == username and parts[6] == password:
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
                abrir_ventana_registrar_usuario()
                return

    messagebox.showerror("Error", "Credenciales incorrectas")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")
    root.title("Login")

    tk.Label(root, text="UserName:").place(x=10, y=20)
    entry_username_login = tk.Entry(root)
    entry_username_login.place(x=10, y=40)

    tk.Label(root, text="Password:").place(x=10, y=70)
    entry_password_login = tk.Entry(root, show="*")
    entry_password_login.place(x=10, y=90)

    btn_login = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion)
    btn_login.place(x=10, y=120)

    if not os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "w") as file:
            pass

    # Cargar usuarios registrados al iniciar la aplicación
    with open("usuarios.txt", "r") as file:
        usuarios_registrados = set()
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                usuarios_registrados.add(parts[0])

btn_vehiculos = tk.Button(ventanaUsuario,
                          text="Vehículos")
btn_vehiculos.place(x=538, y=1)
btn_clientes = tk.Button(ventanaUsuario,
                         text="Clientes", command=abrir_ventana_clientes)
btn_clientes.place(x=485, y=1)

tk.Label(ventanaUsuario, text="ID:").place(x=10, y=10)
entry_id = tk.Entry(ventanaUsuario)
entry_id.place(x=150, y=10)

tk.Label(ventanaUsuario, text="Nombre:").place(x=10, y=40)
entry_nombre = tk.Entry(ventanaUsuario)
entry_nombre.place(x=150, y=40)

tk.Label(ventanaUsuario, text="Apellido Paterno:").place(x=10, y=70)
entry_apellido_paterno = tk.Entry(ventanaUsuario)
entry_apellido_paterno.place(x=150, y=70)

tk.Label(ventanaUsuario, text="Apellido Materno:").place(x=10, y=100)
entry_apellido_materno = tk.Entry(ventanaUsuario)
entry_apellido_materno.place(x=150, y=100)

tk.Label(ventanaUsuario, text="Teléfono:").place(x=10, y=130)
entry_telefono = tk.Entry(ventanaUsuario)
entry_telefono.place(x=150, y=130)

tk.Label(ventanaUsuario, text="UserName:").place(x=10, y=160)
entry_username = tk.Entry(ventanaUsuario)
entry_username.place(x=150, y=160)

tk.Label(ventanaUsuario, text="Password:").place(x=10, y=190)
entry_password = tk.Entry(ventanaUsuario, show="*")
entry_password.place(x=150, y=190)

tk.Label(ventanaUsuario, text="Dirección:").place(x=10, y=220)
entry_direccion = tk.Entry(ventanaUsuario)
entry_direccion.place(x=150, y=220)

tk.Label(ventanaUsuario, text="Perfil:").place(x=10, y=250)
perfiles = ["admin", "gerente", "mecanico", "secretaria"]
combo_perfil = tk.StringVar()
combo_perfil.set(perfiles[0])
combo_perfil_menu = tk.OptionMenu(ventanaUsuario, combo_perfil, *perfiles)
combo_perfil_menu.place(x=150, y=250)

tk.Label(ventanaUsuario, text="Buscar Usuario por Nombre o ID:").place(
    x=10, y=280)
entry_buscar = tk.Entry(ventanaUsuario)
entry_buscar.place(x=250, y=280)

btn_buscar = tk.Button(ventanaUsuario, text="Buscar",
                       command=buscar_usuarios)
btn_buscar.place(x=450, y=280)

btn_guardar_cambios = tk.Button(ventanaUsuario, text="Guardar Cambios",
                                command=guardar_cambios)
btn_guardar_cambios.place(x=100, y=330)

btn_clientes = tk.Button(root, text="Clientes", command=abrir_ventana_clientes)
btn_clientes.place(x=485, y=1)

root.mainloop()
