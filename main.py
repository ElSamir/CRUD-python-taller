import tkinter as tk
from tkinter import messagebox, simpledialog
import os


# Función para registrar un nuevo usuario
clientes_registrados = set()
usuarios_registrados = set()
vehiculos_registrados = set()
reparaciones_registradas = set()
piezas_registradas = set()


def registrar_piezas():
    nueva_pieza_id = entry_pieza_id.get()
    nueva_descripcion_pieza = entry_descripcion_pieza.get()
    nuevo_stock = entry_stock.get()

    # Validar que el  ID no esté repetido
    if nueva_pieza_id in piezas_registradas:
        messagebox.showerror("Error", "ID de pieza ya existe")
    else:
        with open("piezas.txt", "a") as file:
            file.write(
                f"{nueva_pieza_id},{nueva_descripcion_pieza},{nuevo_stock}\n")

        piezas_registradas.add(nueva_pieza_id)

        messagebox.showinfo("Éxito", "Pieza registrada con éxito")


def registrar_reparacion():
    # Obtener los datos de la reparación desde las entradas
    nueva_reparacion_id = entry_reparacion_id.get()
    nueva_fecha_entrada = entry_fecha_entrada.get()
    nueva_fecha_salida = entry_fecha_salida.get()
    nuevo_falla = entry_falla.get()
    nueva_cantidad_piezas = entry_cantidad_piezas.get()
    vehiculo_seleccionado = combo_vehiculo_id.get()
    pieza_seleccionada = combo_pieza_id.get()  # Obtener la pieza seleccionada

    # Validar que el  ID no esté repetido
    if nueva_reparacion_id in reparaciones_registradas:
        messagebox.showerror("Error", "Vehiculo ID  o matricula ya existe")
    else:

        # Validar que haya piezas disponibles y que no se utilicen 0
        stock_pieza = obtener_stock_pieza(pieza_seleccionada)
        if stock_pieza <= 0:
            messagebox.showerror("Error", "No hay piezas disponibles.")
            return
        if int(nueva_cantidad_piezas) <= 0:
            messagebox.showerror(
                "Error", "La cantidad de piezas debe ser mayor que 0.")
            return

        # Restar la cantidad de piezas utilizadas al stock
        nuevo_stock_pieza = stock_pieza - int(nueva_cantidad_piezas)

        # Actualizar el stock en el archivo de piezas
        with open("piezas.txt", "r") as file:
            lines = file.readlines()

        with open("piezas.txt", "w") as file:
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) >= 2 and parts[0] == pieza_seleccionada:
                    line = f"{parts[0]},{parts[1]},{nuevo_stock_pieza}\n"
                file.write(line)

         # Guardar la información de la reparación en el archivo de reparaciones
        with open("reparaciones.txt", "a") as file:
            file.write(
                f"{nueva_reparacion_id},{nueva_fecha_entrada},{nueva_fecha_salida},{nuevo_falla},{nueva_cantidad_piezas},{vehiculo_seleccionado}\n")

        messagebox.showinfo("Éxito", "Reparación registrada exitosamente")


def registrar_cliente():
    nuevo_cliente_id = entry_cliente_id.get()
    nuevo_nombre = entry_nombre_cliente.get()
    nuevo_apellido_paterno = entry_apellido_paterno_cliente.get()
    nuevo_apellido_materno = entry_apellido_materno_cliente.get()
    usuario_seleccionado = combo_usuario_id.get()

    # Validar que el Cliente ID no esté repetido
    if nuevo_cliente_id in clientes_registrados:
        messagebox.showerror("Error", "Cliente ID ya existe")
    else:
        with open("clientes.txt", "a") as file:
            file.write(
                f"{nuevo_cliente_id},{nuevo_nombre},{nuevo_apellido_paterno},{nuevo_apellido_materno},{usuario_seleccionado}\n")

        clientes_registrados.add(nuevo_cliente_id)

        messagebox.showinfo("Éxito", "Cliente registrado con éxito")


def registrar_vehiculo():
    nuevo_vehiculo_id = entry_vehiculo_id.get()
    nuevo_matricula = entry_matricula.get()
    nuevo_marca = entry_marca.get()
    nuevo_modelo = entry_modelo.get()
    nuevo_fecha = entry_fecha.get()
    cliente_seleccionado = combo_cliente_id.get()

    # Validar que el  ID no esté repetido
    if nuevo_matricula in vehiculos_registrados or nuevo_vehiculo_id in vehiculos_registrados:
        messagebox.showerror("Error", "Vehiculo ID  o matricula ya existe")
    else:
        with open("vehiculos.txt", "a") as file:
            file.write(
                f"{nuevo_vehiculo_id},{nuevo_matricula},{nuevo_marca},{nuevo_modelo},{nuevo_fecha},{cliente_seleccionado}\n")

        vehiculos_registrados.add(nuevo_vehiculo_id)
        vehiculos_registrados.add(nuevo_matricula)

        messagebox.showinfo("Éxito", "Vehiculo registrado con éxito")


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


# Función para buscar usuarios por nombre o ID


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
                line = f"{nuevo_nombre},{nuevo_apellido_paterno},{nuevo_apellido_materno},{nuevo_telefono},{nuevo_username},{nuevo_password},{nuevo_direccion},{nuevo_perfil}\n"
            file.write(line)

        messagebox.showinfo("Éxito", "Cambios guardados exitosamente")


def buscar_clientes():
    buscar_texto1 = entry_buscar1.get().lower()
    clientes_encontrados = []

    with open("clientes.txt", "r") as file:
        for line in file:
            parts1 = line.strip().split(",")
            if len(parts1) >= 2:
                nombre_completo1 = f"{parts1[1]} {parts1[2]}"
                if buscar_texto1 in nombre_completo1.lower() or buscar_texto1 == parts1[0].lower():
                    # Ocultar la contraseña antes de agregar la línea

                    clientes_encontrados.append(
                        parts1)  # Agregar toda la línea

    if clientes_encontrados:
        mostrar_clientes_encontrados(clientes_encontrados)
    else:
        messagebox.showinfo("ClientesEncontrados",
                            "Ningún cliente encontrado.")

# Función para cargar los datos de un usuario en los campos de entrada


def mostrar_clientes_encontrados(clientes_encontrados):
    ventana_clientes_encontrados = tk.Toplevel()
    ventana_clientes_encontrados.geometry("400x300")
    ventana_clientes_encontrados.title("Usuarios Encontrados")

    tk.Label(ventana_clientes_encontrados, text="Clientes encontrados:").pack()

    lista_clientes = tk.Listbox(
        ventana_clientes_encontrados, selectmode=tk.SINGLE)
    lista_clientes.pack()

    for cliente in clientes_encontrados:
        lista_clientes.insert(
            tk.END, f"{cliente[1]} {cliente[2]}, ID: {cliente[0]}")

    def editar_cliente_seleccionado():
        seleccion1 = lista_clientes.curselection()
        if seleccion1:
            seleccion_index1 = seleccion1[0]
            cliente_seleccionado = clientes_encontrados[seleccion_index1]
            cargar_datos_cliente(cliente_seleccionado)

    btn_editar = tk.Button(ventana_clientes_encontrados,
                           text="Editar", command=editar_cliente_seleccionado)
    btn_editar.pack()

    def cargar_datos_cliente(cliente):
        entry_cliente_id.delete(0, tk.END)
        entry_cliente_id.insert(0, cliente[0])
        entry_nombre_cliente.delete(0, tk.END)
        entry_nombre_cliente.insert(0, cliente[1])
        entry_apellido_paterno_cliente.delete(0, tk.END)
        entry_apellido_paterno_cliente.insert(0, cliente[2])
        entry_apellido_materno_cliente.delete(0, tk.END)
        entry_apellido_materno_cliente.insert(0, cliente[3])
        combo_usuario_id.set(cliente[4])

# Función para guardar los cambios de la edición


def guardar_cambios_cliente():
    nuevo_cliente_id = entry_cliente_id.get()
    nuevo_nombre = entry_nombre_cliente.get()
    nuevo_apellido_paterno = entry_apellido_paterno_cliente.get()
    nuevo_apellido_materno = entry_apellido_materno_cliente.get()
    usuario_seleccionado = combo_usuario_id.get()

    with open("clientes.txt", "r") as file:
        lines = file.readlines()

    with open("clientes.txt", "w") as file:
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 2 and parts[0] == nuevo_cliente_id:
                line = f"{nuevo_cliente_id},{nuevo_nombre},{nuevo_apellido_paterno},{nuevo_apellido_materno},{usuario_seleccionado}\n"
            file.write(line)

        messagebox.showinfo("Éxito", "Cambios guardados exitosamente")


def buscar_vehiculos():
    buscar_texto3 = entry_buscar3.get().lower()
    vehiculos_encontrados = []

    with open("vehiculos.txt", "r") as file:
        for line in file:
            parts2 = line.strip().split(",")
            if len(parts2) >= 2:
                modelo_placa = f"{parts2[1]} {parts2[3]}"
                if buscar_texto3 == parts2[0].lower():

                    vehiculos_encontrados.append(
                        parts2)  # Agregar toda la línea

    if vehiculos_encontrados:
        mostrar_vehiculos_encontrados(vehiculos_encontrados)
    else:
        messagebox.showinfo("Vehículos Encontrados",
                            "Ningún vehículo encontrado.")

# Función para cargar los datos de un usuario en los campos de entrada


def mostrar_vehiculos_encontrados(vehiculos_encontrados):
    ventana_vehiculos_encontrados = tk.Toplevel()
    ventana_vehiculos_encontrados.geometry("400x300")
    ventana_vehiculos_encontrados.title("Vehículos Encontrados")

    tk.Label(ventana_vehiculos_encontrados,
             text="Vehiculos encontrados:").pack()

    lista_vehiculos = tk.Listbox(
        ventana_vehiculos_encontrados, selectmode=tk.SINGLE)
    lista_vehiculos.pack()

    for vehiculo in vehiculos_encontrados:
        lista_vehiculos.insert(
            tk.END, f"{vehiculo[1]} {vehiculo[2]}, ID: {vehiculo[0]}")

    def editar_vehiculo_seleccionado():
        seleccion2 = lista_vehiculos.curselection()
        if seleccion2:
            seleccion_index2 = seleccion2[0]
            vehiculo_seleccionado = vehiculos_encontrados[seleccion_index2]
            cargar_datos_vehiculo(vehiculo_seleccionado)

    btn_editar = tk.Button(ventana_vehiculos_encontrados,
                           text="Editar", command=editar_vehiculo_seleccionado)
    btn_editar.pack()

    def cargar_datos_vehiculo(vehiculo):
        entry_vehiculo_id.delete(0, tk.END)
        entry_vehiculo_id.insert(0, vehiculo[0])
        entry_matricula.delete(0, tk.END)
        entry_matricula.insert(0, vehiculo[1])
        entry_marca.delete(0, tk.END)
        entry_marca.insert(0, vehiculo[2])
        entry_modelo.delete(0, tk.END)
        entry_modelo.insert(0, vehiculo[3])
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, vehiculo[4])
        combo_cliente_id.set(vehiculo[5])

# Función para guardar los cambios de la edición


def guardar_cambios_vehiculo():
    nuevo_vehiculo_id = entry_vehiculo_id.get()
    nuevo_matricula = entry_matricula.get()
    nuevo_marca = entry_marca.get()
    nuevo_modelo = entry_modelo.get()
    nuevo_fecha = entry_fecha.get()
    cliente_seleccionado = combo_cliente_id.get()

    with open("vehiculos.txt", "r") as file:
        lines = file.readlines()

    with open("vehiculos.txt", "w") as file:
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 2 and parts[0] == nuevo_vehiculo_id:
                line = f"{nuevo_vehiculo_id},{nuevo_matricula},{nuevo_marca},{nuevo_modelo},{nuevo_fecha},{cliente_seleccionado}\n"
            file.write(line)

        messagebox.showinfo("Éxito", "Cambios guardados exitosamente")


def buscar_reparaciones():
    buscar_texto4 = entry_buscar4.get().lower()
    reparaciones_encontradas = []

    with open("reparaciones.txt", "r") as file:
        for line in file:
            parts3 = line.strip().split(",")
            if len(parts3) >= 2:
                id_de_reparacion = f"{parts3[0]} "
                if buscar_texto4 == parts3[0].lower():

                    reparaciones_encontradas.append(
                        parts3)  # Agregar toda la línea

    if reparaciones_encontradas:
        mostrar_reparaciones_encontradas(reparaciones_encontradas)
    else:
        messagebox.showinfo("Reparaciones Encontradas",
                            "Ningúna reparacion encontrada.")

# Función para cargar los datos de un usuario en los campos de entrada


def mostrar_reparaciones_encontradas(reparaciones_encontradas):
    ventana_reparaciones_encontradas = tk.Toplevel()
    ventana_reparaciones_encontradas.geometry("400x300")
    ventana_reparaciones_encontradas.title("Vehículos Encontrados")

    tk.Label(ventana_reparaciones_encontradas,
             text="Reparacioness encontradas:").pack()

    lista_reparaciones = tk.Listbox(
        ventana_reparaciones_encontradas, selectmode=tk.SINGLE)
    lista_reparaciones.pack()

    for reparacion in reparaciones_encontradas:
        lista_reparaciones.insert(
            tk.END, f"{reparacion[1]} {reparacion[2]}, ID: {reparacion[0]}")

    def editar_reparacion_seleccionada():
        seleccion3 = lista_reparaciones.curselection()
        if seleccion3:
            seleccion_index3 = seleccion3[0]
            reparacion_seleccionada = reparaciones_encontradas[seleccion_index3]
            cargar_datos_reparacion(reparacion_seleccionada)

    btn_editarR = tk.Button(ventana_reparaciones_encontradas,
                            text="Editar", command=editar_reparacion_seleccionada)
    btn_editarR.pack()

    def cargar_datos_reparacion(reparacion):
        entry_reparacion_id.delete(0, tk.END)
        entry_reparacion_id.insert(0, reparacion[0])
        entry_fecha_entrada.delete(0, tk.END)
        entry_fecha_entrada.insert(0, reparacion[1])
        entry_fecha_salida.delete(0, tk.END)
        entry_fecha_salida.insert(0, reparacion[2])
        entry_falla.delete(0, tk.END)
        entry_falla.insert(0, reparacion[3])
        entry_cantidad_piezas.delete(0, tk.END)
        entry_cantidad_piezas.insert(0, reparacion[4])
        combo_vehiculo_id.set(reparacion[5])


# Función para guardar los cambios de la edición


def guardar_cambios_reparacion():

    nueva_reparacion_id = entry_reparacion_id.get()
    nueva_fecha_entrada = entry_fecha_entrada.get()
    nueva_fecha_salida = entry_fecha_salida.get()
    nuevo_falla = entry_falla.get()
    nuevo_cantidad_piezas = entry_cantidad_piezas.get()
    vehiculo_seleccionado = combo_vehiculo_id.get()

    with open("reparaciones.txt", "r") as file:
        lines = file.readlines()

    with open("reparaciones.txt", "w") as file:
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 2 and parts[0] == nueva_reparacion_id:
                line = f"{nueva_reparacion_id},{nueva_fecha_entrada},{nueva_fecha_salida},{nuevo_falla},{nuevo_cantidad_piezas},{vehiculo_seleccionado}\n"
            file.write(line)

        messagebox.showinfo("Éxito", "Cambios guardados exitosamente")


def buscar_piezas():
    buscar_texto5 = entry_buscar5.get().lower()
    piezas_encontradas = []

    with open("piezas.txt", "r") as file:
        for line in file:
            parts4 = line.strip().split(",")
            if len(parts4) >= 2:
                id_de_pieza = f"{parts4[0]} "
                if buscar_texto5 == parts4[0].lower():

                    piezas_encontradas.append(
                        parts4)  # Agregar toda la línea

    if piezas_encontradas:
        mostrar_piezas_encontradas(piezas_encontradas)
    else:
        messagebox.showinfo("Piezas Encontradas",
                            "Ningúna pieza encontrada.")

# Función para cargar los datos de un usuario en los campos de entrada


def mostrar_piezas_encontradas(piezas_encontradas):
    ventana_piezas_encontradas = tk.Toplevel()
    ventana_piezas_encontradas.geometry("400x300")
    ventana_piezas_encontradas.title("Vehículos Encontrados")

    tk.Label(ventana_piezas_encontradas,
             text="Piezas encontradas:").pack()

    lista_piezas = tk.Listbox(
        ventana_piezas_encontradas, selectmode=tk.SINGLE)
    lista_piezas.pack()

    for pieza in piezas_encontradas:
        lista_piezas.insert(
            tk.END, f"{pieza[1]} {pieza[2]}, ID: {pieza[0]}")

    def editar_pieza_seleccionada():
        seleccion4 = lista_piezas.curselection()
        if seleccion4:
            seleccion_index4 = seleccion4[0]
            pieza_seleccionada = piezas_encontradas[seleccion_index4]
            cargar_datos_pieza(pieza_seleccionada)

    btn_editarR = tk.Button(ventana_piezas_encontradas,
                            text="Editar", command=editar_pieza_seleccionada)
    btn_editarR.pack()

    def cargar_datos_pieza(pieza):
        entry_pieza_id.delete(0, tk.END)
        entry_pieza_id.insert(0, pieza[0])
        entry_descripcion_pieza.delete(0, tk.END)
        entry_descripcion_pieza.insert(0, pieza[1])
        entry_stock.delete(0, tk.END)
        entry_stock.insert(0, pieza[2])


# Función para guardar los cambios de la edición


def guardar_cambios_pieza():

    nueva_pieza_id = entry_pieza_id.get()
    nueva_descripcion_pieza = entry_descripcion_pieza.get()
    nuevo_stock = entry_stock.get()

    with open("piezas.txt", "r") as file:
        lines = file.readlines()

    with open("piezas.txt", "w") as file:
        for line in lines:
            parts = line.strip().split(",")
            if len(parts) >= 2 and parts[0] == nueva_pieza_id:
                line = f"{nueva_pieza_id},{nueva_descripcion_pieza},{nuevo_stock}\n"
            file.write(line)

        messagebox.showinfo("Éxito", "Cambios guardados exitosamente")


def abrir_ventana_pieza():
    global ventanaPiezas, entry_buscar5, entry_pieza_id, entry_descripcion_pieza, entry_stock
    ventanaPiezas = tk.Toplevel()
    ventanaPiezas.geometry("600x500")
    ventanaPiezas.title("Registrar Pieza")

    tk.Label(ventanaPiezas, text="Pieza ID:").place(x=10, y=10)
    entry_pieza_id = tk.Entry(ventanaPiezas)
    entry_pieza_id.place(x=150, y=10)

    tk.Label(ventanaPiezas, text="Descripcion:").place(x=10, y=40)
    entry_descripcion_pieza = tk.Entry(ventanaPiezas)
    entry_descripcion_pieza.place(x=150, y=40)

    tk.Label(ventanaPiezas, text="Cantidad:").place(x=10, y=70)
    entry_stock = tk.Entry(ventanaPiezas)
    entry_stock.place(x=150, y=70)

    btn_registrar_pieza = tk.Button(
        ventanaPiezas, text="Registrar Pieza", command=registrar_piezas)
    btn_registrar_pieza.place(x=10, y=190)

    tk.Label(ventanaPiezas, text="Buscar Pieza por ID:").place(
        x=10, y=220)
    entry_buscar5 = tk.Entry(ventanaPiezas)
    entry_buscar5.place(x=250, y=220)

    btn_buscar = tk.Button(ventanaPiezas, text="Buscar",
                           command=buscar_piezas)
    btn_buscar.place(x=450, y=220)

    btn_guardar_cambios = tk.Button(ventanaPiezas, text="Guardar Cambios",
                                    command=guardar_cambios_pieza)
    btn_guardar_cambios.place(x=100, y=250)


def abrir_ventana_reparacion():
    global ventanaReparaciones, entry_buscar4, entry_reparacion_id, entry_fecha_entrada, entry_fecha_salida, entry_falla, entry_cantidad_piezas, combo_vehiculo_id, combo_pieza_id

    ventanaReparaciones = tk.Toplevel()
    ventanaReparaciones.geometry("600x500")
    ventanaReparaciones.title("Registrar Reparacion")

    tk.Label(ventanaReparaciones, text="Reparacion ID:").place(x=10, y=10)
    entry_reparacion_id = tk.Entry(ventanaReparaciones)
    entry_reparacion_id.place(x=150, y=10)

    tk.Label(ventanaReparaciones, text="Fecha de entrada:").place(x=10, y=40)
    entry_fecha_entrada = tk.Entry(ventanaReparaciones)
    entry_fecha_entrada.place(x=150, y=40)

    tk.Label(ventanaReparaciones, text="Fecha de salida:").place(x=10, y=70)
    entry_fecha_salida = tk.Entry(ventanaReparaciones)
    entry_fecha_salida.place(x=150, y=70)

    tk.Label(ventanaReparaciones, text="Falla:").place(x=10, y=130)
    entry_falla = tk.Entry(ventanaReparaciones)
    entry_falla.place(x=150, y=130)

    tk.Label(ventanaReparaciones, text="Piezas:").place(x=10, y=100)
    entry_cantidad_piezas = tk.Entry(ventanaReparaciones)
    entry_cantidad_piezas.place(x=150, y=100)

    # Selector para elegir la ID de la pieza
    tk.Label(ventanaReparaciones, text="Selecciona Pieza ID:").place(x=10, y=190)
    combo_pieza_id = tk.StringVar()
    combo_pieza_id.set("")  # Valor inicial en blanco

    # Obtener una lista de IDs de piezas registradas
    piezas_disponibles = [
        pieza for pieza in piezas_registradas if obtener_stock_pieza(pieza) > 0]

    combo_pieza_id_menu = tk.OptionMenu(
        ventanaReparaciones, combo_pieza_id, *piezas_disponibles)
    combo_pieza_id_menu.place(x=200, y=190)

    tk.Label(ventanaReparaciones,
             text="Selecciona Vehiculo ID:").place(x=10, y=160)
    combo_vehiculo_id = tk.StringVar()
    combo_vehiculo_id.set("")  # Valor inicial en blanco
    combo_vehiculo_id_menu = tk.OptionMenu(
        ventanaReparaciones, combo_vehiculo_id, *vehiculos_registrados)
    combo_vehiculo_id_menu.place(x=200, y=160)

    btn_registrar_reparacion = tk.Button(
        ventanaReparaciones, text="Registrar Reparacion", command=registrar_reparacion)
    btn_registrar_reparacion.place(x=10, y=210)

    tk.Label(ventanaReparaciones, text="Buscar Reparacion por ID:").place(
        x=10, y=250)
    entry_buscar4 = tk.Entry(ventanaReparaciones)
    entry_buscar4.place(x=250, y=250)

    btn_buscar = tk.Button(ventanaReparaciones, text="Buscar",
                           command=buscar_reparaciones)
    btn_buscar.place(x=450, y=250)

    btn_guardar_cambios = tk.Button(ventanaReparaciones, text="Guardar Cambios",
                                    command=guardar_cambios_reparacion)
    btn_guardar_cambios.place(x=100, y=300)


def obtener_stock_pieza(id_pieza):
    # Función para obtener el stock de una pieza por su ID
    with open("piezas.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 2 and parts[0] == id_pieza:
                # El stock se encuentra en la tercera posición
                return int(parts[2])

    return 0  # Si no se encuentra la pieza, se asume que el stock es 0


def abrir_ventana_vehiculos():
    global ventanaVehiculos, entry_buscar3, entry_buscar2, entry_vehiculo_id, entry_matricula, entry_marca, entry_modelo, entry_fecha, combo_cliente_id
    ventanaVehiculos = tk.Toplevel()
    ventanaVehiculos.geometry("600x500")
    ventanaVehiculos.title("Registrar Vehiculo")

    tk.Label(ventanaVehiculos, text="Vehiculo ID:").place(x=10, y=10)
    entry_vehiculo_id = tk.Entry(ventanaVehiculos)
    entry_vehiculo_id.place(x=150, y=10)

    tk.Label(ventanaVehiculos, text="Matricula:").place(x=10, y=40)
    entry_matricula = tk.Entry(ventanaVehiculos)
    entry_matricula.place(x=150, y=40)

    tk.Label(ventanaVehiculos, text="Marca:").place(x=10, y=70)
    entry_marca = tk.Entry(ventanaVehiculos)
    entry_marca.place(x=150, y=70)

    tk.Label(ventanaVehiculos, text="Modelo:").place(x=10, y=100)
    entry_modelo = tk.Entry(ventanaVehiculos)
    entry_modelo.place(x=150, y=100)

    tk.Label(ventanaVehiculos, text="Fecha:").place(x=10, y=130)
    entry_fecha = tk.Entry(ventanaVehiculos)
    entry_fecha.place(x=150, y=130)
    # Obtener una lista de IDs de usuarios registrados

    # Selector para elegir la ID del usuario registrado
    tk.Label(ventanaVehiculos, text="Seleccionar Cliente ID:").place(x=10, y=160)
    combo_cliente_id = tk.StringVar()
    combo_cliente_id.set("")  # Valor inicial en blanco
    combo_cliente_id_menu = tk.OptionMenu(
        ventanaVehiculos, combo_cliente_id, *clientes_registrados)
    combo_cliente_id_menu.place(x=200, y=160)

    btn_registrar_vehiculo = tk.Button(
        ventanaVehiculos, text="Registrar Vehiculo", command=registrar_vehiculo)
    btn_registrar_vehiculo.place(x=10, y=190)

    tk.Label(ventanaVehiculos, text="Buscar Vehículo por ID:").place(
        x=10, y=220)
    entry_buscar3 = tk.Entry(ventanaVehiculos)
    entry_buscar3.place(x=250, y=220)

    btn_buscar = tk.Button(ventanaVehiculos, text="Buscar",
                           command=buscar_vehiculos)
    btn_buscar.place(x=450, y=220)

    btn_guardar_cambios = tk.Button(ventanaVehiculos, text="Guardar Cambios",
                                    command=guardar_cambios_vehiculo)
    btn_guardar_cambios.place(x=100, y=250)


# Dentro de la función abrir_ventana_clientes

def abrir_ventana_clientes():
    global ventanaClientes, entry_buscar1, entry_cliente_id, entry_nombre_cliente, entry_apellido_paterno_cliente, entry_apellido_materno_cliente, combo_usuario_id

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

    # Obtener una lista de IDs de usuarios registrados

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

    tk.Label(ventanaClientes, text="Buscar Cliente por Nombre o ID:").place(
        x=10, y=190)
    entry_buscar1 = tk.Entry(ventanaClientes)
    entry_buscar1.place(x=250, y=190)

    btn_buscar = tk.Button(ventanaClientes, text="Buscar",
                           command=buscar_clientes)
    btn_buscar.place(x=450, y=190)

    btn_guardar_cambios = tk.Button(ventanaClientes, text="Guardar Cambios",
                                    command=guardar_cambios_cliente)
    btn_guardar_cambios.place(x=100, y=250)


def abrir_ventana_registrar_usuario():
    global ventanaUsuario, entry_id, entry_nombre, entry_apellido_paterno, entry_apellido_materno, entry_telefono, entry_username, entry_password, entry_direccion, combo_perfil, entry_buscar

    ventanaUsuario = tk.Toplevel()
    ventanaUsuario.geometry("600x500")
    ventanaUsuario.title("Registrar Usuario")

    btn_registrar = tk.Button(
        ventanaUsuario, text="Registrar", command=registrar_usuario)
    btn_registrar.place(x=10, y=330)

    btn_vehiculos = tk.Button(
        ventanaUsuario, text="Vehículos", command=abrir_ventana_vehiculos)
    btn_vehiculos.place(x=412, y=1)
    btn_clientes = tk.Button(
        ventanaUsuario, text="Clientes", command=abrir_ventana_clientes)
    btn_clientes.place(x=359, y=1)
    btn_reparaciones = tk.Button(
        ventanaUsuario, text="Reparaciones", command=abrir_ventana_reparacion)
    btn_reparaciones.place(x=516, y=1)
    btn_piezas = tk.Button(
        ventanaUsuario, text="Piezas", command=abrir_ventana_pieza)
    btn_piezas.place(x=474, y=1)

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


# Función para realizar el inicio de sesión


def iniciar_sesion():
    username = entry_username_login.get()
    password = entry_password_login.get()

    if not os.path.exists("usuarios.txt"):
        with open("usuarios.txt", "w") as file:
            pass

    with open("usuarios.txt", "r") as file:
        usuarios_registrados = set()
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 2:
                usuarios_registrados.add(parts[0])

    # Verificar si las credenciales son válidas
    with open("usuarios.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 6 and parts[5] == username and parts[6] == password:
                messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
                abrir_ventana_registrar_usuario()
                return

    messagebox.showerror("Error", "Credenciales incorrectas")


# Crear una ventana principal
root = tk.Tk()

root.geometry("400x300")


root.title("Login")

tk.Label(root, text="UserName:").place(x=10, y=20)
entry_username_login = tk.Entry(root)
entry_username_login.place(x=10, y=40)

tk.Label(root, text="Password:").place(x=10, y=70)
entry_password_login = tk.Entry(root, show="*")
entry_password_login.place(x=10, y=90)

btn_login = tk.Button(root, text="Iniciar Sesión", command=iniciar_sesion)
btn_login.place(x=10, y=120)


if not os.path.exists("piezas.txt"):
    with open("piezas.txt", "w") as file:
        pass

with open("piezas.txt", "r") as file:
    piezas_registradas = set()
    for line in file:
        parts = line.strip().split(",")
        if len(parts) >= 2:
            piezas_registradas.add(parts[0])

if not os.path.exists("piezas.txt"):
    with open("piezas.txt", "w") as file:
        pass

with open("reparaciones.txt", "r") as file:
    reparaciones_registradas = set()
    for line in file:
        parts = line.strip().split(",")
        if len(parts) >= 2:
            reparaciones_registradas.add(parts[0])


if not os.path.exists("vehiculos.txt"):
    with open("vehiculos.txt", "w") as file:
        pass

with open("vehiculos.txt", "r") as file:
    vehiculos_registrados_registrados = set()
    for line in file:
        parts = line.strip().split(",")
        if len(parts) >= 2:
            vehiculos_registrados.add(parts[0])

if not os.path.exists("clientes.txt"):
    with open("clientes.txt", "w") as file:
        pass

with open("clientes.txt", "r") as file:
    usuarios_registrados = set()
    for line in file:
        parts = line.strip().split(",")
        if len(parts) >= 2:
            clientes_registrados.add(parts[0])

if not os.path.exists("usuarios.txt"):
    with open("usuarios.txt", "w") as file:
        pass

with open("usuarios.txt", "r") as file:
    usuarios_registrados = set()
    for line in file:
        parts = line.strip().split(",")
        if len(parts) >= 2:
            usuarios_registrados.add(parts[0])


root.mainloop()
