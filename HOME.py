import sqlite3
import tkinter as tk
import datetime
import tkcalendar
from tkinter import messagebox, ttk

import Dependencias
import Personas
import Arbol_de_Dependencias_2
import Informes
import Arbol_de_Dependencias_1

# Variables globales para almacenar el ID de usuario y el ID del organigrama
user_id = 0
org_id = 0

conexion = sqlite3.connect('organigrama.db')
cursor = conexion.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS organigrama (ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, FECHA TEXT, '
    'USUARIO_ID INTEGER)')
cursor.execute(
    'CREATE TABLE IF NOT EXISTS usuario (ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, CONTRA TEXT)')


class VentanaPrincipal(tk.Tk):
    def __init__(self, auxiliar_user_id):
        tk.Tk.__init__(self)
        global user_id
        user_id = auxiliar_user_id

        # Configuración de la ventana principal
        self.geometry("600x450")
        self.title("ORGANIGRAMAS")
        self.resizable(False, False)

        # Creación de los frames y botones
        self.Crear_Frames()
        self.Crear_Botones()
        self.pos_ventanas()
        self.C_sesion()
        self.Lista_Organigramas = []

        # Atributo para extraer matriz organigrama asociado al usuario que inició sesión
        self.extraer_organigramas()

        # Mostrar la lista de dependencias asociadas a ese usuario en pantalla
        self.MostrarLista()

    # ==================================================================================================================
    # ===============================================FRAMES Y BOTONES===================================================
    # ==================================================================================================================

    def Crear_Frames(self):
        """
        Crea y configura los frames utilizados en la interfaz.
        Crea los frames: frame_arriba, frame_lista y frame_botones.
        Configura el tamaño de los frames.
        Ubica los frames utilizando el administrador de geometría grid.
        Configura las filas y columnas para adaptarse al tamaño de la ventana.
        Crea y configura un Listbox en el frame_lista.
        Crea y configura el título "BIENVENIDO AL GESTOR DE ORGANIGRAMAS" en el centro del frame_arriba.
        """
        # Creación de los frames
        self.frame_arriba = tk.Frame(self, bg="#FF2525", bd=1, relief="ridge")
        self.frame_lista = tk.Frame(self, bg="#FFFFFF")
        self.frame_botones = tk.Frame(self, bg="#FF2525", bd=1, relief="ridge")

        # Tamaño de los frames
        self.frame_arriba.config(height=180)
        self.frame_botones.config(width=200)
        self.frame_lista.config(height=300)

        # Ubicación de los frames utilizando el administrador de geometría grid
        self.frame_arriba.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.frame_botones.grid(row=1, column=0, sticky="nsew")
        self.frame_lista.grid(row=1, column=1, sticky="nsew")

        # Configuración de las filas y columnas para que se adapten al tamaño de la ventana
        self.grid_rowconfigure(0, weight=0)  # Ajuste el peso a 0 para evitar la redimensión vertical
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.lista_box = tk.Listbox(self.frame_lista, bg="#F0F0F0", bd=0, relief="flat", selectbackground="#E0E0E0")
        self.lista_box.pack(fill="both", expand=True, padx=5, pady=5)
        self.lista_box.config(selectmode="SINGLE")

        # Creación del título "ORGANIGRAMA" en el centro del frame_arriba
        title_label = tk.Label(self.frame_arriba, text="BIENVENIDO AL GESTOR DE ORGANIGRAMAS",
                               font=("Segoe UI Black", 16, "bold"), fg="#FFFFFF", bg="#FF2525")
        title_label.place(relx=0.1, rely=0.4)


    def Crear_Botones(self):
        """
        Crea y configura los botones en el frame_botones.
        Crea botones para realizar diversas acciones relacionadas con el proyecto y el organigrama.
        Configura los botones para llamar a los métodos correspondientes cuando se hace clic en ellos.
        """
        # Creación de los botones en el frame_botones
        separador_label = tk.Label(self.frame_botones, text="_____________Proyecto______________",
                                   font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
        separador_label.place(x=0)

        btn_crear = tk.Button(self.frame_botones, text="Crear", bg="white", fg="black", font=("Arial", 9, "bold"),
                              command=self.Crear)
        btn_crear.place(x=15 + 12, y=30)

        btn_eliminar = tk.Button(self.frame_botones, text="Eliminar", bg="white", fg="black", font=("Arial", 9, "bold"),
                                 command=self.Eliminar)
        btn_eliminar.place(x=105 + 15, y=30)

        btn_editar = tk.Button(self.frame_botones, text="Editar", bg="white", fg="black", font=("Arial", 9, "bold"),
                               command=self.Editar)
        btn_editar.place(x=60 + 15, y=30)

        separador2_label = tk.Label(self.frame_botones, text="__________Organigrama____________",
                                    font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
        separador2_label.place(x=0, y=60)

        btn_editar = tk.Button(self.frame_botones, text="Copiar", bg="white", fg="black", font=("Arial", 9, "bold"),
                               width=23, command=self.Copiar)
        btn_editar.place(x=10, y=100)

        btn_a_organigrama = tk.Button(self.frame_botones, bg="white", fg="black", font=("Arial", 9, "bold"),
                                      text="Abrir Organigrama", width=23, command=self.Abrir_Organigrama)
        btn_a_organigrama.place(x=10, y=170 - 30)

        btn_a_organigrama = tk.Button(self.frame_botones, bg="white", fg="black", font=("Arial", 9, "bold"),
                                      text="Graficar Organigrama", width=23, command=self.Ventana_Graficar_Organigrama)
        btn_a_organigrama.place(x=10, y=210 - 30)

        btn_a_organigrama = tk.Button(self.frame_botones, bg="white", fg="black", font=("Arial", 9, "bold"),
                                      text="Informes", width=23, command=self.informes)
        btn_a_organigrama.place(x=10, y=250 - 30)


    def cerrar_sesion(self):
        # Cerrar la ventana actual
        self.destroy()

        # Abrir la ventana de inicio de sesión
        from LOGIN import VentanaInicioSesion
        ventana_inicio_sesion = VentanaInicioSesion()
        ventana_inicio_sesion.mainloop()

    # ==================================================================================================================
    # ==========================================CREAR ORGANIGRAMA=======================================================
    # ==================================================================================================================

    def Crear(self):
        """
        Crea una nueva ventana para crear un nuevo proyecto.
        Configura la apariencia y tamaño de la ventana de creación.
        Crea los campos de entrada para el nombre del proyecto y la fecha de creación.
        """
        v_crear = tk.Toplevel(self)
        v_crear.config(bg="#FF2525")
        v_crear.geometry("430x80")
        v_crear.title("CREAR NUEVO PROYECTO")
        v_crear.resizable(False, False)
        self.pos_ventana_crear(v_crear)

        # Creación de los campos de entrada (entry widgets)
        nombre_label = tk.Label(v_crear, text="Nombre del Proyecto", font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
        nombre_label.place(x=0, y=5)

        self.nombre_entry = tk.Entry(v_crear, width=43, highlightbackground="#E5D8D8", highlightcolor="#E5D8D8", highlightthickness=1)
        self.nombre_entry.place(x=160, y=5)

        fecha_label = tk.Label(v_crear, text="Fecha de creacion", font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
        fecha_label.place(x=0, y=46)

        self.fecha_entry = tkcalendar.DateEntry(v_crear, width=12, date_pattern="dd/mm/yyyy", bg="#FF2525")
        self.fecha_entry.set_date(datetime.date.today())
        self.fecha_entry.place(x=160, y=46)

        def validar_agregar():
            """
            Realiza la validación y el proceso de agregar un nuevo elemento.
            Obtiene el nombre y la fecha ingresados por el usuario.
            Verifica que el nombre no esté vacío.
            Consulta la base de datos para verificar si el nombre ya existe para el usuario actual.
            Si el nombre ya existe, muestra un mensaje de error.
            Si el nombre no existe, inserta los valores en la base de datos.
            Muestra un mensaje de éxito y limpia los campos de entrada.
            Actualiza el contenido del Listbox en el frame_lista.
            """
            nombre = self.nombre_entry.get()
            fecha = self.fecha_entry.get_date().strftime('%d/%m/%Y')

            if nombre == "":
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return

            if len(nombre) < 1 or len(nombre) > 25:
                messagebox.showerror("Error", "El nombre debe tener entre 1 y 25 caracteres.")
                return

                # Verificar si el nombre ya existe en la base de datos y obtener su ID
            cursor.execute('SELECT * FROM organigrama WHERE NOMBRE = ? and USUARIO_ID = ?', (nombre, user_id))
            result = cursor.fetchone()

            if result is not None:
                messagebox.showerror("Error", "El nombre ingresado ya existe.")
                return

            # Insertar los valores en la base de datos
            cursor.execute('INSERT INTO organigrama (nombre, fecha, usuario_id) VALUES (?, ?, ?)', (nombre, fecha, user_id))
            conexion.commit()

            cursor.execute('SELECT ID FROM organigrama WHERE nombre = ?', (nombre,))
            result = cursor.fetchone()
            org_id = result[0]

            print("Se ha insertado en la base de datos:\n"
                  f"Nombre del organigrama: {nombre}\n"
                  f"Fecha de creacion del organigrama: {fecha}\n"
                  f"ID del usuario al que esta asociado este organigrama: {user_id}\n"
                  f"Este organigrama tiene como ID: {org_id}\n")

            # Limpiar los campos de entrada
            self.nombre_entry.delete(0, tk.END)
            self.fecha_entry.set_date(datetime.date.today())

            # Mostrar mensaje de éxito
            messagebox.showinfo("Mensaje", "Proyecto creado.")

            # Cerrar la ventana v_crear
            v_crear.destroy()

            # Actualizar el contenido del Listbox en el frame_lista
            self.MostrarLista()

        # Creación del botón "Agregar" con validación
        btn_agregar = tk.Button(v_crear, text="Agregar", bg="white", fg="black", font=("Arial", 10), width=8,
                                command=validar_agregar)
        btn_agregar.place(x=270, y=40)

        # Función para limpiar los campos de entrada
        def limpiar_campos():
            """
            Limpia el contenido del campo de entrada de nombre.
            """
            self.nombre_entry.delete(0, tk.END)

        # Creación del botón "Limpiar" con función para limpiar campos
        btn_limpiar = tk.Button(v_crear, text="Limpiar", bg="white", fg="black", font=("Arial", 10), width=8,
                                command=limpiar_campos)
        btn_limpiar.place(x=350, y=40)


    def Agregar(self, codigo_entry, nombre_entry, fecha_entry):
        """
        Agrega un nuevo proyecto a la lista de organigramas.
        Obtiene el código, nombre y fecha ingresados por el usuario.
        Crea un diccionario con los datos del proyecto.
        Agrega el diccionario a la lista de organigramas.
        Actualiza el contenido del Listbox en el frame_lista.
        Muestra un mensaje de éxito.
        """
        codigo = codigo_entry.get()
        nombre = nombre_entry.get()
        fecha = fecha_entry.get_date()

        organigrama = {
            'codigo': codigo,
            'nombre': nombre,
            'fecha': fecha
        }

        self.Lista_Organigramas.append(organigrama)

        # Actualizar el contenido del Listbox en el frame_lista
        self.MostrarLista()

        # Mostrar mensaje de éxito
        messagebox.showinfo("Mensaje", "Proyecto creado.")


    def obtener_org_id_seleccionado(self):
        """
        Obtiene el ID del organigrama seleccionado en el Listbox.
        Obtiene el índice del elemento seleccionado en el Listbox.
        Si hay un elemento seleccionado, obtiene el nombre y la fecha del organigrama.
        Busca el ID del organigrama en la base de datos utilizando el nombre y la fecha.
        Si se encuentra el organigrama en la base de datos, devuelve su ID.
        Si no se encuentra el organigrama en la base de datos, muestra un mensaje de error.
        Si no hay un organigrama seleccionado, muestra un mensaje indicando que no se ha seleccionado ningún organigrama.
        """
        # Obtener el índice del elemento seleccionado en el Listbox
        seleccionado = self.lista_box.curselection()

        if seleccionado:
            indice = seleccionado[0]
            elemento_seleccionado = self.lista_box.get(indice)

            # Obtener el nombre y la fecha separados por "|"
            nombre, fecha = elemento_seleccionado.split(" | ")
            fecha = fecha.strip()
            nombre = nombre.strip()

            print(f"NOMBRE DEL ORGANIGRAMA SELECCIONADO: {nombre}\n"
                  f"FECHA DEL ORGANIGRAMA SELECCIONADO: {fecha}\n")

            # Buscar el ID del organigrama en la tabla organigrama
            cursor.execute('SELECT ID FROM organigrama WHERE nombre = ? AND fecha = ?', (nombre, fecha))
            resultado = cursor.fetchone()

            if resultado:
                org_id = resultado[0]
                print(f"EL ID DEL ORGANIGRAMA SELECCIONADO ES: {org_id}")
                return org_id
            else:
                print("No se encontró el organigrama seleccionado en la base de datos.")
                return None
        else:
            print("No se ha seleccionado ningún organigrama.")
            return None

    # ==================================================================================================================
    # ==========================================ELIMINAR ORGANIGRAMA====================================================
    # ==================================================================================================================

    def Eliminar(self):
        """
        Elimina el organigrama seleccionado. Obtiene el ID del organigrama seleccionado. Consulta la base de datos
        para obtener las personas y dependencias asociadas al organigrama.
        Muestra un mensaje de confirmación con las dependencias y personas a eliminar.
        Si se confirma la eliminación, procede a eliminar las dependencias, actualizar las personas y eliminar el
        organigrama. Muestra mensajes de éxito o cancelación de la eliminación.
        """
        org_id = self.obtener_org_id_seleccionado()

        if org_id:
            # Obtener los datos de las personas que cumplen con la condición
            cursor.execute('SELECT NOM, APE, PUE FROM personas WHERE ORG_ID = ?', (org_id,))
            personas_a_eliminar = cursor.fetchall()

            # Obtener las dependencias asociadas al organigrama
            cursor.execute('SELECT Nombre FROM dependencias WHERE ORG_ID = ?', (org_id,))
            dependencias = cursor.fetchall()

            # Mostrar mensaje de confirmación
            mensaje_confirmacion = "¿Estás seguro que quieres eliminar este organigrama?\n\n"

            # Imprime en pantalla las dependencias que se van a eliminar e imprime hasta 15 para evitar que la ventana
            # sea demasiado grande.
            if dependencias:
                mensaje_confirmacion += "Se eliminarán las siguientes dependencias:\n"
                for dependencia in dependencias[:15]:
                    mensaje_confirmacion += f"{dependencia[0]}\n"
                if len(dependencias) > 15:
                    mensaje_confirmacion += "...\n"
            else:
                mensaje_confirmacion += "(Sin dependencias asociadas)\n"

            mensaje_confirmacion += "\n"

            # Imprime en pantalla las personas que se van a eliminar e imprime hasta 15 para evitar que la ventana
            # sea demasiado grande.
            if personas_a_eliminar:
                mensaje_confirmacion += "Y los datos de las siguientes personas:\n"
                for persona in personas_a_eliminar[:15]:
                    mensaje_confirmacion += f"{persona[0]} {persona[1]}, {persona[2]}\n"
                if len(personas_a_eliminar) > 15:
                    mensaje_confirmacion += "...\n"
            else:
                mensaje_confirmacion += "(Sin personas asociadas)\n"

            # Mostrar ventana de confirmación
            confirmado = messagebox.askokcancel("Confirmar eliminación", mensaje_confirmacion)

            if confirmado:
                # Eliminar dependencias asociadas al organigrama
                cursor.execute('DELETE FROM dependencias WHERE ORG_ID = ?', (org_id,))
                conexion.commit()

                # Eliminar las personas asociadas al organigrama
                cursor.execute('DELETE FROM personas WHERE ORG_ID = ?', (org_id,))
                conexion.commit()

                # Eliminar el organigrama
                cursor.execute('DELETE FROM organigrama WHERE ID = ?', (org_id,))
                conexion.commit()

                messagebox.showinfo("Eliminado", "Se ha eliminado el organigrama con éxito.")
                self.MostrarLista()
            else:
                messagebox.showinfo("Cancelado", "La eliminación ha sido cancelada.")
        else:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un elemento para eliminar.")

    # ==================================================================================================================
    # ==========================================COPIAR ORGANIGRAMA======================================================
    # ==================================================================================================================

    def Copiar(self):
        """
        Realiza la copia de un organigrama seleccionado.
        Obtiene el ID del organigrama seleccionado.
        Verifica que se haya seleccionado un organigrama.
        Consulta la base de datos para obtener los datos del organigrama seleccionado.
        Genera un nuevo nombre para la copia del organigrama.
        Verifica si el nombre ya existe en la tabla organigrama.
        Si el nombre ya existe, agrega un contador al final del nombre.
        Crea una copia del organigrama seleccionado con el nuevo nombre.
        Obtiene las dependencias del organigrama seleccionado.
        Crea un diccionario para mapear los IDs originales a los nuevos IDs.
        Inserta las dependencias copiadas y actualiza las referencias a las dependencias padre.
        Obtiene las personas del organigrama seleccionado.
        Actualiza el ORG_ID de las personas copiadas.
        Actualiza el contenido del Listbox.
        Muestra un mensaje de copia realizada.
        """
        # Obtener el ID del organigrama seleccionado
        org_id = self.obtener_org_id_seleccionado()
        print("ORG ID DENTRO DEL METODO COPIAR:", org_id)

        if org_id:
            # Obtener los datos del organigrama seleccionado
            conexion = sqlite3.connect('organigrama.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT NOMBRE, FECHA FROM organigrama WHERE ID = ?', (org_id,))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                nombre_organigrama, fecha_organigrama = resultado

                # Generar un nuevo nombre para la copia del organigrama
                nuevo_nombre = nombre_organigrama + " - copia"

                # Verificar si el nombre ya existe en la tabla organigrama
                conexion = sqlite3.connect('organigrama.db')
                cursor = conexion.cursor()
                cursor.execute('SELECT COUNT(*) FROM organigrama WHERE NOMBRE LIKE ?', (nuevo_nombre + '%',))
                count = cursor.fetchone()[0]
                conexion.close()

                # Si el nombre ya existe, agregar un contador al final del nombre
                if count > 0:
                    nuevo_nombre += f" ({count})"

                # Crear una copia del organigrama seleccionado con el nuevo nombre
                conexion = sqlite3.connect('organigrama.db')
                cursor = conexion.cursor()
                cursor.execute('INSERT INTO organigrama (NOMBRE, FECHA, USUARIO_ID) VALUES (?, ?, ?)',
                               (nuevo_nombre, fecha_organigrama, user_id))
                nuevo_org_id = cursor.lastrowid

                # Obtener las dependencias del organigrama seleccionado
                cursor.execute('SELECT ID, NOMBRE, DEPENDENCIA_PADRE_ID, ORG_ID FROM dependencias WHERE ORG_ID = ?',
                               (org_id,))
                dependencias = cursor.fetchall()

                # Crear un diccionario para mapear los IDs originales a los nuevos IDs
                id_mapping = {}

                # Insertar la dependencia principal en la tabla "dependencias"
                cursor.execute('SELECT NOMBRE FROM dependencias WHERE DEPENDENCIA_PADRE_ID = 0 AND ORG_ID = ?',
                               (org_id,))
                dependencia_principal = cursor.fetchone()

                if dependencia_principal:
                    dependencia_principal_nombre = dependencia_principal[0]
                    cursor.execute('INSERT INTO dependencias (NOMBRE, DEPENDENCIA_PADRE_ID, ORG_ID) VALUES (?, ?, ?)',
                                   (dependencia_principal_nombre, 0, nuevo_org_id))
                    id_mapping[0] = cursor.lastrowid

                # Insertar las dependencias copiadas y actualizar las referencias a las dependencias padre
                for dependencia in dependencias:
                    dependencia_id = dependencia[0]
                    dependencia_nombre = dependencia[1]
                    dependencia_padre_id = dependencia[2]

                    if dependencia_padre_id is not None:
                        nueva_dependencia_padre_id = id_mapping.get(dependencia_padre_id)
                    else:
                        nueva_dependencia_padre_id = None

                    # Verificar si la dependencia ya ha sido copiada
                    cursor.execute(
                        'SELECT COUNT(*) FROM dependencias WHERE NOMBRE = ? AND ORG_ID = ?',
                        (dependencia_nombre, nuevo_org_id))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        # Insertar la dependencia copiada en la tabla "dependencias"
                        cursor.execute('INSERT INTO dependencias (NOMBRE, DEPENDENCIA_PADRE_ID, ORG_ID) VALUES (?, ?, ?)',
                                       (dependencia_nombre, nueva_dependencia_padre_id, nuevo_org_id))
                        nueva_dependencia_id = cursor.lastrowid

                        # Actualizar el diccionario de mapeo
                        id_mapping[dependencia_id] = nueva_dependencia_id

                # Obtener las personas del organigrama seleccionado
                cursor.execute(
                    'SELECT ID, CED, NOM, APE, TEL, DIR, DEP, SAL, NAC, PUE, ORG_ID FROM personas WHERE ORG_ID = ?',
                    (org_id,))
                personas = cursor.fetchall()
                print("PERSONAS:", personas)

                # Actualizar el ORG_ID de las personas copiadas
                for persona in personas:
                    cursor.execute(
                        'INSERT INTO personas (CED, NOM, APE, TEL, DIR, DEP, SAL, NAC, PUE, ORG_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        (persona[1], persona[2], persona[3], persona[4], persona[5], persona[6], persona[7], persona[8],
                         persona[9], nuevo_org_id))

                conexion.commit()
                conexion.close()

                messagebox.showinfo("Copia realizada",
                                    "Se ha realizado la copia del organigrama seleccionado correctamente.")

                # Actualizar el contenido del Listbox
                self.MostrarLista()

        else:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un organigrama para copiar.")

    # ==================================================================================================================
    # ==========================================EDITAR ORGANIGRAMA======================================================
    # ==================================================================================================================

    def Editar(self):
        """
        Permite editar un proyecto seleccionado en el Listbox.
        Obtiene el índice del elemento seleccionado en el Listbox.
        Si se ha seleccionado un proyecto:
            Obtiene los datos del proyecto desde la base de datos.
            Crea una ventana de edición de proyecto.
            Muestra los campos de edición con los datos existentes.
            Define una función para guardar los cambios.
            Verifica el formato de la fecha ingresada.
            Verifica si el nuevo nombre ya existe para el usuario actual.
            Conecta a la base de datos y actualiza los datos del proyecto.
            Actualiza el contenido del Listbox.
            Muestra un mensaje de cambios guardados.
            Cierra la ventana de edición de proyecto.
        Si no se ha seleccionado un proyecto, muestra un mensaje de advertencia.
        """
        # Obtener el índice del elemento seleccionado en el Listbox
        org_id = self.obtener_org_id_seleccionado()

        if org_id:
            # Obtener los datos del organigrama desde la base de datos
            conexion = sqlite3.connect('organigrama.db')
            cursor = conexion.cursor()
            cursor.execute('SELECT NOMBRE, FECHA, USUARIO_ID FROM organigrama WHERE ID = ?', (org_id,))
            resultado = cursor.fetchone()
            conexion.close()

            if resultado:
                nombre_organigrama, fecha_organigrama, usuario_id_existente = resultado

                # Crear la ventana de edición de proyecto
                v_editar = tk.Toplevel(self)
                v_editar.config(bg="#FF2525")
                v_editar.geometry("430x80")
                v_editar.title("EDITAR PROYECTO")
                v_editar.resizable(False, False)
                self.pos_ventana_editar(v_editar)

                # Crear los campos de edición
                nombre_label = tk.Label(v_editar, text="Nombre del Proyecto", font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
                nombre_label.place(x=0, y=5)
                self.nombre_entry = tk.Entry(v_editar, width=43, highlightbackground="#E5D8D8", highlightcolor="#E5D8D8", highlightthickness=1)
                self.nombre_entry.insert(0, nombre_organigrama)
                self.nombre_entry.place(x=160, y=5)

                fecha_label = tk.Label(v_editar, text="Fecha de creacion", font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
                fecha_label.place(x=0, y=46)

                self.fecha_entry = tk.Entry(v_editar)
                self.fecha_entry.insert(0, fecha_organigrama)
                self.fecha_entry.place(x=160, y=46)

                # Función para guardar los cambios
                def guardar_cambios():
                    """
                    Guarda los cambios realizados en el organigrama.
                    Obtiene los nuevos valores del nombre y la fecha ingresados por el usuario.
                    Verifica el formato de la fecha y muestra un mensaje de error si es incorrecto.
                    Verifica si el nuevo nombre ya existe para el usuario actual y muestra un mensaje de error si es el caso.
                    Conecta a la base de datos y actualiza los datos del organigrama con los nuevos valores.
                    Actualiza el contenido del Listbox.
                    Muestra un mensaje de cambios guardados exitosamente.
                    Cierra la ventana de edición de proyecto.
                    """
                    # Obtener los nuevos valores del nombre y la fecha
                    nuevo_nombre = self.nombre_entry.get()
                    nueva_fecha_str = self.fecha_entry.get()

                    # Verificar el formato de la fecha
                    try:
                        nueva_fecha = datetime.datetime.strptime(nueva_fecha_str, "%d/%m/%Y").date()
                    except ValueError:
                        messagebox.showwarning("Formato de fecha incorrecto", "El formato de fecha debe ser dd/mm/aaaa.")
                        return

                    # Convertir la fecha al formato "DD/MM/YYYY" antes de guardarla en la base de datos
                    nueva_fecha_formatted = nueva_fecha.strftime("%d/%m/%Y")

                    # Verificar si el nuevo nombre ya existe para el usuario actual
                    conexion = sqlite3.connect('organigrama.db')
                    cursor = conexion.cursor()
                    cursor.execute('SELECT NOMBRE FROM organigrama WHERE USUARIO_ID = ?', (user_id,))
                    nombres_existentes = cursor.fetchall()
                    conexion.close()

                    for nombre_existente in nombres_existentes:
                        if nombre_existente[0] == nuevo_nombre and usuario_id_existente == user_id:
                            messagebox.showwarning("Nombre existente", "Ese nombre ya existe.")
                            return

                    # Conectar a la base de datos y actualizar los datos del organigrama
                    conexion = sqlite3.connect('organigrama.db')
                    cursor = conexion.cursor()
                    cursor.execute('UPDATE organigrama SET NOMBRE = ?, FECHA = ? WHERE ID = ?', (nuevo_nombre, nueva_fecha_formatted, org_id))
                    conexion.commit()
                    conexion.close()

                    # Actualizar el contenido del Listbox
                    self.MostrarLista()

                    messagebox.showinfo("Cambios guardados", "Los cambios han sido guardados correctamente.")

                    # Cerrar la ventana de edición de proyecto
                    v_editar.destroy()

                # Crear el botón para guardar los cambios
                btn_agregar = tk.Button(v_editar, text="Guardar Cambios", bg="white", fg="black", font=("Arial", 10), command=guardar_cambios)
                btn_agregar.place(x=300, y=40)


        else:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un elemento para editar.")

    # ==================================================================================================================
    # ==========================================ABRIR ORGANIGRAMA=======================================================
    # ==================================================================================================================

    def Abrir_Organigrama(self):
        """
        Abre una ventana para mostrar y modificar un organigrama seleccionado.
        Obtiene el ID del organigrama seleccionado.
        Si no se ha seleccionado ningún organigrama, muestra un mensaje de advertencia.
        Si se ha seleccionado un organigrama, abre una nueva ventana.
        Configura la apariencia y propiedades de la nueva ventana.
        Crea y coloca los elementos de la ventana, como títulos y botones.
        Asigna funciones a los botones para agregar, modificar y eliminar dependencias y personas.
        """
        org_id = self.obtener_org_id_seleccionado()
        print("EL ID DEL ORGANIGRAMA QUE SE LLEVARA A MODIFICAR ES: ", org_id)
        if org_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un elemento para abrir.")
        else:
            v_abrir = tk.Toplevel(self)
            v_abrir.geometry("330x120")
            v_abrir.config(bg="#FF2525")
            v_abrir.title("Dependencias y Personas")
            v_abrir.resizable(False, False)
            self.pos_ventana_crear(v_abrir)

            # Titulos
            titulo1 = tk.Label(v_abrir, text="____________________Dependencias___________________",
                               font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
            titulo1.place(x=20, y=5)

            agregarDependencia_button = tk.Button(v_abrir, text="Agregar, Modificar y Eliminar Dependencias", bg="white",
                                                  fg="black", font=("Arial", 9, "bold"), width=40,
                                                  command=self.agregar_y_modificar_dependencias)
            agregarDependencia_button.place(x=20, y=30)

            titulo2 = tk.Label(v_abrir, text="_______________________Personas______________________",
                               font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
            titulo2.place(x=20, y=60)

            personas_button = tk.Button(v_abrir, text="Agregar, Modificar y Eliminar Personas", bg="white", fg="black",
                                        font=("Arial", 9, "bold"), width=40, command=self.Agregar_y_Modificar_Personas)
            personas_button.place(x=20, y=90)

    # ==================================================================================================================
    # ======================================GENERAR INFORMES DE ORGANIGRAMA=============================================
    # ==================================================================================================================
    def informes(self):
        """
        Abre la ventana de informes.
        Obtiene el ID del organigrama seleccionado.
        Si se ha seleccionado un organigrama, abre la ventana de informes con el ID del organigrama.
        Si no se ha seleccionado ningún organigrama, muestra un mensaje de error.
        """
        org_id = self.obtener_org_id_seleccionado()
        if org_id is None:
            # Mostrar un mensaje de advertencia si no se seleccionó ningún elemento
            messagebox.showwarning('Error', 'No ha seleccionado ningún organigrama')

        else:
            self.destroy()

            Informes.VInformes(org_id=org_id)


    def agregar_y_modificar_dependencias(self):
        """
        Realiza la acción de agregar y modificar dependencias para un organigrama seleccionado.
        Obtiene el ID del organigrama seleccionado.
        Imprime el ID del organigrama que se modificará.
        Verifica si se ha seleccionado un organigrama.
        Si no se ha seleccionado ningún elemento, muestra un mensaje de advertencia.
        Si se ha seleccionado un organigrama, destruye la ventana actual.
        Ejecuta la función "ejecutar_dependencias" pasando el ID del organigrama.
        """
        # Obtener el ID del organigrama seleccionado
        org_id = self.obtener_org_id_seleccionado()

        # Imprimir el ID del organigrama que se modificará
        print("EL ID DEL ORGANIGRAMA QUE SE LLEVARÁ A MODIFICAR ES: ", org_id)

        # Verificar si se seleccionó un organigrama
        if org_id is None:
            # Mostrar un mensaje de advertencia si no se seleccionó ningún elemento
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un elemento para abrir.")
        else:
            # Destruir la ventana actual
            self.destroy()

            # Ejecutar la función "ejecutar_dependencias" pasando el ID del organigrama
            Dependencias.ejecutar_dependencias(org_id)


    def Agregar_y_Modificar_Personas(self):
        """
        Verifica si se ha seleccionado un elemento del organigrama.
        Si no se ha seleccionado, muestra un mensaje de advertencia.
        Si se ha seleccionado, destruye la ventana actual y llama a la función "Abrir_Vincular" del módulo "Personas"
        pasando el ID del organigrama seleccionado como argumento.
        """
        org_id = self.obtener_org_id_seleccionado()
        print("EL ID DEL ORGANIGRAMA QUE SE LLEVARA A MODIFICAR ES:", org_id)

        if org_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un elemento para abrir.")
        else:
            self.destroy()
            # Llamar a la función "Abrir_Vincular" del módulo "Personas"
            Personas.Abrir_Vincular(org_id)

    # ==================================================================================================================
    # ===========================================GRAFICAR ORGANIGRAMA===================================================
    # ==================================================================================================================

    def Ventana_Graficar_Organigrama(self):
        """
        Abre una ventana para seleccionar opciones de graficado del organigrama.
        Obtiene el ID del organigrama seleccionado.
        Si no se ha seleccionado un elemento, muestra un mensaje de advertencia.
        Si se ha seleccionado un elemento, muestra la ventana de opciones de graficado.
        Permite al usuario seleccionar entre graficar el organigrama completo o desde una dependencia.
        Muestra una entrada para seleccionar la dependencia en caso de seleccionar esa opción.
        Al graficar, se llama a las funciones correspondientes según la opción seleccionada.
        """
        org_id = self.obtener_org_id_seleccionado()
        print("EL ID DEL ORGANIGRAMA QUE SE LLEVARA A MODIFICAR ES: ", org_id)

        if org_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un elemento para graficar.")
        else:
            v_organigrama = tk.Toplevel(self)
            v_organigrama.geometry("330x200")
            v_organigrama.config(bg="#FF2525")
            v_organigrama.title("Dependencias y Personas")
            v_organigrama.resizable(False, False)
            self.pos_ventana_crear(v_organigrama)

            # Titulo
            titulo1 = tk.Label(v_organigrama, text="_______________________Graficar_______________________",
                               font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
            titulo1.place(x=20, y=5)

            # Variable para almacenar la opción seleccionada
            opcion_seleccionada = tk.StringVar()

            # Lista para almacenar las dependencias
            dependencias_list = []

            # Función para mostrar u ocultar la Entry dependiendo de la opción seleccionada
            def mostrar_entrada_dependencia():
                if opcion_seleccionada.get() == "dependencia":
                    additional_entry_label.place(x=20, y=90)
                    additional_entry.place(x=30, y=120)
                    cargar_dependencias()
                else:
                    additional_entry_label.place_forget()
                    additional_entry.place_forget()

            # Función para cargar las dependencias disponibles en la Entry
            def cargar_dependencias():
                # Conectar a la base de datos
                conexion = sqlite3.connect("organigrama.db")
                cursor = conexion.cursor()

                # Consulta SQL para obtener las dependencias específicas
                org_id = self.obtener_org_id_seleccionado()
                consulta = "SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?"
                cursor.execute(consulta, (org_id,))

                # Obtener los resultados de la consulta
                dependencias = cursor.fetchall()

                # Cerrar el cursor y la conexión a la base de datos
                cursor.close()
                conexion.close()

                # Limpiar la lista de dependencias
                dependencias_list.clear()

                # Agregar las dependencias a la lista y actualizar los valores del Combobox
                for dependencia in dependencias:
                    dependencias_list.append(dependencia[0])

                additional_entry['values'] = dependencias_list

            # Función para graficar dependiendo de la opción seleccionada
            def graficar(org_id):
                if opcion_seleccionada.get() == "completo":
                    self.Graficar_Organigrama()
                elif opcion_seleccionada.get() == "dependencia":
                    dependencia_seleccionada = additional_entry.get()
                    print("ORG ID EN GRAFICAR ES: ", org_id)
                    self.Graficar_OrganigramaDesdeDependencia(dependencia_seleccionada, org_id)

            # Configuración del color de fondo de los checkbuttons
            style = ttk.Style()
            style.configure("TCheckbutton", background="#FF2525", foreground="white", font=("Arial", 9, "bold"))

            # Checkbutton para seleccionar organigrama completo
            completo_checkbutton = ttk.Checkbutton(v_organigrama, text="Organigrama completo", style="TCheckbutton",
                                                   variable=opcion_seleccionada, onvalue="completo", offvalue="")
            completo_checkbutton.place(x=20, y=30)

            # Checkbutton para seleccionar organigrama desde una dependencia
            dependencia_checkbutton = ttk.Checkbutton(v_organigrama, text="Organigrama desde una dependencia",
                                                      style="TCheckbutton",
                                                      variable=opcion_seleccionada, onvalue="dependencia", offvalue="")
            dependencia_checkbutton.place(x=20, y=70)

            # Etiqueta y Combobox para seleccionar una dependencia
            additional_entry_label = tk.Label(v_organigrama, text="Se graficará desde: ", bg="#FF2525")
            additional_entry = ttk.Combobox(v_organigrama, values=dependencias_list)

            # Obtener el ID del organigrama antes de presionar el botón de graficar.
            org_id = self.obtener_org_id_seleccionado()

            # Botón para graficar
            graficar_button = tk.Button(
                v_organigrama,
                text="Graficar",
                bg="white",
                fg="black",
                font=("Arial", 9, "bold"),
                width=40,
                command=lambda: graficar(org_id)
            )
            graficar_button.place(x=20, y=150)

            # Asociar función de mostrar/ocultar la Entry al cambio de selección
            opcion_seleccionada.trace("w", lambda *args: mostrar_entrada_dependencia())


    def Graficar_Organigrama(self):
        """
        Genera y muestra el gráfico del organigrama seleccionado.
        Obtiene el ID del organigrama seleccionado.
        Si no se ha seleccionado ningún organigrama, muestra un mensaje de advertencia.
        Si se ha seleccionado un organigrama, obtiene los departamentos y la raíz del organigrama.
        Si el organigrama no tiene departamentos ni una dependencia de mando, muestra un mensaje de error.
        Si el organigrama no tiene departamentos, muestra un mensaje de error.
        Si el organigrama no tiene una dependencia de mando, muestra un mensaje de error.
        Si se cumplen todas las condiciones anteriores, intenta crear el árbol de dependencias y mostrarlo.
        Si ocurre un error durante el proceso, muestra un mensaje de error.
        """
        org_id = self.obtener_org_id_seleccionado()
        print("EL ID DEL ORGANIGRAMA QUE SE LLEVARA A MODIFICAR ES: ", org_id)

        if org_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un para graficar.")
        else:
            # Obtener los departamentos
            cursor.execute("SELECT * FROM dependencias WHERE DEPENDENCIA_PADRE_ID IS NULL AND ORG_ID = ?", (org_id,))
            departamentos = cursor.fetchall()

            cursor.execute("SELECT * FROM dependencias WHERE ORG_ID = ? AND DEPENDENCIA_PADRE_ID = 0", (org_id,))
            raiz = cursor.fetchone()

            if len(departamentos) == 0 and raiz is None:
                messagebox.showerror("Error", "Este organigrama no posee una dependencia de mando ni departamentos.")
            elif len(departamentos) == 0:
                messagebox.showerror("Error", "Este organigrama no posee ningún departamento.")
            elif raiz is None:
                messagebox.showerror("Error", "Este organigrama no posee una dependencia de mando.")
            else:
                try:
                    org_id = self.obtener_org_id_seleccionado()
                    self.destroy()  # Destruir la ventana actual
                    Arbol_de_Dependencias_2.crear_arbol(org_id)
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                except Exception as e:
                    messagebox.showerror("Error", "Se produjo un error al generar el árbol: " + str(e))
                else:
                    print("Árbol de dependencias generado exitosamente")

    def Graficar_OrganigramaDesdeDependencia(self, dependencia_seleccionada, org_id):
        """
        Grafica un organigrama a partir de una dependencia seleccionada.
        Recibe la dependencia seleccionada y el ID del organigrama.
        Verifica si se ha seleccionado un organigrama.
        Si no se ha seleccionado, muestra un mensaje de advertencia.
        Si se ha seleccionado, busca el ID de la dependencia seleccionada en la base de datos.
        Verifica si la dependencia tiene subdependencias asociadas.
        Si no tiene subdependencias, muestra un mensaje de error.
        Si tiene subdependencias, crea el árbol de dependencias y destruye la ventana actual.
        Muestra mensajes de error en caso de excepciones o errores.
        """
        if org_id is None:
            messagebox.showwarning("No seleccionado", "Por favor, seleccione un organigrama para graficar.")
        else:
            print("DEPENDENCIA SELECCIONADA EN GRAFICAR ORGANIGRAMA DESDE UNA DEPENDENCIA", dependencia_seleccionada)
            print("ORG_ID EN GRAFICAR ORGANIGRAMA DESDE UNA DEPENDENCIA", org_id)

            # Buscar en la base de datos el ID de la dependencia seleccionada.
            try:
                cursor.execute("SELECT COUNT(*) FROM dependencias WHERE DEPENDENCIA_PADRE_ID = ? AND ORG_ID = ?",
                               (self.buscar_dependencia_id(dependencia_seleccionada, org_id), org_id))
                count = cursor.fetchone()[0]
                if count == 0:
                    raise ValueError("No se puede graficar este organigrama porque esta dependencia no tiene subdependencias asociadas o porque esta dependencia es la dependencia de mayor rango")
                self.destroy()  # Destruir la ventana actual
                Arbol_de_Dependencias_1.crear_arbol(dependencia_seleccionada, org_id)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", "Se produjo un error al generar el árbol: " + str(e))
            else:
                print("Árbol de dependencias generado exitosamente")

    # ==================================================================================================================
    # =====================================GENERAR Y ORDENAR DATOS DE INTERFAZ==========================================
    # ==================================================================================================================

    def buscar_dependencia_id(self, dependencia_seleccionada, org_id):
        """
        Busca el ID de una dependencia en la base de datos.
        Recibe el nombre de la dependencia seleccionada y el ID de el organigrama.
        Realiza una consulta a la base de datos para obtener el ID de la dependencia.
        Si se encuentra el resultado, devuelve el ID de la dependencia.
        Si no se encuentra el resultado, devuelve None.

        Parámetros:
        - dependencia_seleccionada (str): Nombre de la dependencia seleccionada.
        - org_id (int): ID del organigrama seleccionado.

        Retorna:
        - dependencia_seleccionada_id (int or None): ID de la dependencia seleccionada o None si no se encuentra.

        """
        cursor.execute("SELECT ID FROM dependencias WHERE NOMBRE = ? AND ORG_ID = ?", (dependencia_seleccionada, org_id))
        result = cursor.fetchone()
        if result:
            dependencia_seleccionada_id = result[0]
            return dependencia_seleccionada_id
        else:
            return None


    def extraer_organigramas(self):
        """
        Extrae los organigramas asociados al usuario actual desde la base de datos.
        Realiza una consulta a la base de datos para obtener los organigramas asociados al user_id.
        Almacena los valores obtenidos en una matriz.
        Retorna la matriz de organigramas.
        """
        # Realizar la consulta a la base de datos para obtener los organigramas asociados al user_id
        print("USER ID:", user_id)
        cursor.execute('SELECT nombre, fecha FROM organigrama WHERE usuario_id = ?', (user_id,))
        organigramas = cursor.fetchall()

        # Almacenar los valores en una matriz
        matriz_organigramas = []

        for organigrama in organigramas:
            nombre = organigrama[0]
            fecha = organigrama[1]
            matriz_organigramas.append([nombre, fecha])

        print(f"LA MATRIZ ORGANIGRAMA ASOCIADA A ESTE USUARIO: {matriz_organigramas}")

        return matriz_organigramas


    def MostrarLista(self):
        """
        Actualiza el contenido del Listbox con la lista de organigramas.
        Limpia el contenido actual del Listbox.
        Obtiene una matriz de organigramas mediante la función extraer_organigramas.
        Agrega los datos de cada organigrama al Listbox, mostrando el nombre y la fecha.
        Ajusta la longitud del campo "nombre" en función de la longitud máxima del código.
        Configura la fuente del Listbox.
        """
        # Limpiar el contenido actual del Listbox
        self.lista_box.delete(0, tk.END)
        matriz_organigramas = self.extraer_organigramas()

        # Agregar los datos de matriz_organigramas al Listbox
        for organigrama in matriz_organigramas:
            nombre = organigrama[0]
            fecha = organigrama[1]
            # Ajustar la longitud del campo "nombre" en función de la longitud máxima del código
            self.lista_box.insert(tk.END, f"{nombre}  |  {fecha}")

        font_size = 10
        self.lista_box.configure(font=("Arial", font_size))


    def pos_ventanas(self):
        """
        Centra la ventana en la pantalla.
        Calcula el ancho y largo actual de la ventana.
        Calcula las coordenadas (x, y) para centrar la ventana en la pantalla.
        Actualiza la geometría de la ventana para que se muestre centrada.
        """
        self.update_idletasks()
        ancho = self.winfo_width()
        largo = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (largo // 2)
        self.geometry('{}x{}+{}+{}'.format(ancho, largo, x, y))


    def pos_ventana_crear(self, ventana_crear):
        """
        Posiciona la ventana de creación en una ubicación específica.
        Recibe la ventana de creación como parámetro.
        Establece las coordenadas (x, y) para la ubicación de la ventana.
        """
        x = 30
        y = 160
        ventana_crear.geometry('+{}+{}'.format(x, y))


    def pos_ventana_editar(self, ventana_crear):
        """
        Posiciona la ventana de edición en una ubicación específica.
        Recibe la ventana de creación como parámetro.
        Establece las coordenadas (x, y) para la ubicación de la ventana.
        """
        x = 30
        y = 400
        ventana_crear.geometry('+{}+{}'.format(x, y))


    def C_sesion(self):
        """
        Crea un botón para cerrar la sesión.
        Crea un botón en el frame_arriba con el texto "Cerrar Sesion".
        Configura el color, fuente y comando del botón.
        Establece las coordenadas (x, y) para la ubicación del botón.
        """
        btn_c_sesion = tk.Button(self.frame_arriba, text="Cerrar Sesion", bg="white", fg="black", font=("Arial", 9, "bold"), command=self.cerrar_sesion)
        btn_c_sesion.place(x=507, y=150)


    def __del__(self):
        """
        Método especial para liberar recursos y cerrar la conexión a la base de datos.
        Cierra la conexión a la base de datos al destruir el objeto.
        """
        # Cerrar la conexión a la base de datos
        conexion.close()
