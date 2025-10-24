import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.font import Font

conexion = sqlite3.connect('organigrama.db')
cursor = conexion.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS dependencias (ID INTEGER PRIMARY KEY AUTOINCREMENT, NOMBRE TEXT, DEPENDENCIA_PADRE_ID INTEGER, ORG_ID INTEGER)')

class Agregar_y_modificar_dependencias(tk.Tk):
    def __init__(self, org_id):
        tk.Tk.__init__(self)

        self.org_id = org_id            #id del organigrama para asociarlas a las dependencias que se van creando.
        print("org_id es dentro de agregar y modificar dependencias:", org_id)
        self.dependencia_id = None      # id de la dependencia para utilzar en la modificacion de las dependencias.
        self.dependencias_hijas = []    # Lista para almacenar las dependencias hijas
        # Para la entrada adicional al presionar que se va a asociar la dependencia a otra dependencia padre.
        self.show_additional_entry = BooleanVar()
        self.title("Dependencias")

        self.frame = tk.Frame(self)
        self.geometry("600x450")
        self.config(bg="#FF2525")
        self.resizable(False, False)
        self.frame.grid(row=0, column=0)
        self.frame_botones_inferiores = tk.Frame(self)
        self.frame_botones_inferiores.grid(row=1, column=0)

        self.botones = tk.LabelFrame(self.frame,bg="#FF2525",bd=0, relief="groove")
        self.botones.grid(row=0, column=0)

        self.etiqueta_agregar_buttom = tk.Button(self.botones, text="AGREGAR",bg="white", fg="black", font=("Arial", 9, "bold"),command=self.crear_interfaz_agregar)
        self.etiqueta_agregar_buttom.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)
        self.etiqueta_agregar_buttom.config(width=8, height=1)

        self.etiqueta_eliminar_buttom = tk.Button(self.botones, text="MODIFICAR",bg="white", fg="black", font=("Arial", 9, "bold"),command=self.crear_interfaz_modificar)
        self.etiqueta_eliminar_buttom.grid(row=1, column=2, sticky="nsew", padx=10, pady=5)

        self.etiqueta_modificar_buttom = tk.Button(self.botones, text="ELIMINAR",bg="white", fg="black", font=("Arial", 9, "bold"),command=self.crear_interfaz_eliminar)
        self.etiqueta_modificar_buttom.grid(row=2, column=2, sticky="nsew", padx=10, pady=5)

        self.regresar_vinculo = tk.Button(self.botones, text="REGRESAR",bg="white", fg="black", font=("Arial", 9, "bold") ,command=self.Regresar_A_Inicio)
        self.regresar_vinculo.grid(row=4, column=2, sticky="nsew", padx=10, pady=5)

        self.etiqueta_modificar_buttom = tk.Button(self.botones, text="MOVER",bg="white", fg="black", font=("Arial", 9, "bold"),command=self.crear_interfaz_mover)
        self.etiqueta_modificar_buttom.grid(row=3, column=2, sticky="nsew", padx=10, pady=5)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.botones.columnconfigure(0, weight=1)
        self.botones.rowconfigure(0, weight=1)
        self.botones.rowconfigure(1, weight=1)
        self.botones.rowconfigure(2, weight=1)

        self.update_idletasks()  # Actualizar la interfaz antes de centrar la ventana

        # Obtener el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Obtener el tamaño de la ventana
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Calcular la posición x, y para centrar la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Posicionar la ventana en el centro de la pantalla
        self.geometry(f"+{x}+{y}")

        self.mainloop()

    def buscar_usuario_id(self):
        """
        Busca el ID de usuario asociado a un ID de organigrama en la base de datos.
        Recibe el ID del organigrama como parámetro.
        Consulta la base de datos para obtener el ID de usuario asociado al ID de organigrama.
        Si se encuentra el resultado, devuelve el ID de usuario.
        Si no se encuentra el resultado, devuelve None.
        """
        cursor.execute('SELECT USUARIO_ID FROM organigrama WHERE ID = ?', (self.org_id,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
            print("USUARIO ID EN BUSCAR USUARIO:", user_id)
            return user_id
        else:
            return None

    def Regresar_A_Inicio(self):
        """
        Este es un método para regresar a la ventana principal.
        Regresa a la ventana principal, no recibe ningún parámetro.
        """
        user_id = self.buscar_usuario_id()  # Invocar al método con paréntesis para obtener el resultado
        print("USUARIO ID EN REGRESAR A INICIO:", user_id)
        self.destroy()
        from HOME import VentanaPrincipal
        print("Se envía la ID DE USUARIO a la ventana principal:", user_id)
        VentanaPrincipal(user_id)
        VentanaPrincipal.mainloop(self)

    # ==================================================================================================================
    # ===================================INTERFAZ DE CREAR LA DEPENDENCIA===============================================
    # ==================================================================================================================

    def crear_interfaz_agregar(self):
        """
        Crea la interfaz gráfica para agregar información de dependencia.

        Define variables de control y configuraciones iniciales.
        Crea y configura los elementos de la interfaz: etiquetas, entradas, botones, etc.
        """
        self.ced = StringVar()
        self.nom = StringVar()
        self.show_additional_entry = BooleanVar(value=False)
        self.mayor_rango_selected = BooleanVar(value=False)

        colorFondo = "#FF2525"
        self.title("Agregar")
        self.frame = tk.LabelFrame(self, bd=4, relief="groove")
        self.frame.grid(row=0, column=0)
        self.tamanho_de_letra = Font(size=15)
        self.frame.config(bg=colorFondo)

        self.user_info_frame = tk.LabelFrame(self.frame, text="Informacion de Dependencia", font=self.tamanho_de_letra,
                                             bd=0, relief="groove")
        self.user_info_frame.grid(row=0, column=0, padx=40, pady=40)
        self.user_info_frame.config(bg=colorFondo)

        self.nombre_label = tk.Label(self.user_info_frame, text="Nombre", bg=colorFondo)
        self.nombre_label.grid(row=0, column=5, sticky="e", pady=5)

        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.nombre_entry.grid(row=0, column=8, sticky="e")

        self.verificar_checkbutton = tk.Checkbutton(self.user_info_frame, text="Estará asociada a otra dependencia",
                                                    bg=colorFondo, variable=self.show_additional_entry,
                                                    command=self.mostrar_entrada_adicional)
        self.verificar_checkbutton.grid(row=1, column=5, columnspan=4, sticky="w")

        self.additional_entry_label = tk.Label(self.user_info_frame, text="Estará asociada a:", bg=colorFondo)
        self.additional_entry = ttk.Combobox(self.user_info_frame, textvariable=self.nom)

        self.verificar_checkbutton2 = tk.Checkbutton(self.user_info_frame, text="Será el mayor rango del organigrama",
                                                     bg=colorFondo, variable=self.mayor_rango_selected,
                                                     command=self.deshabilitar_checkbutton)
        self.verificar_checkbutton2.grid(row=5, column=5, columnspan=4, sticky="w")

        # Obtener lista de departamentos existentes para el organigrama actual
        cursor.execute('SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.additional_entry['values'] = lista_dependencias
        self.additional_entry_label.grid(row=2, column=5, sticky="e")
        self.additional_entry.grid(row=2, column=8, sticky="e")
        self.additional_entry_label.grid_remove()
        self.additional_entry.grid_remove()

        self.etiqueta_agregar_buttom = tk.Button(self.frame, text="AGREGAR", bg="white", fg="black",
                                                 font=("Arial", 9, "bold"),
                                                 command=self.verificar_datos)
        self.etiqueta_agregar_buttom.grid(row=6, column=0, sticky="news", padx=20, pady=1)

        self.etiqueta_regresar_buttom = tk.Button(self.frame, text="REGRESAR", bg="white", fg="black",
                                                  font=("Arial", 9, "bold"),
                                                  command=lambda: self.regresar_entry(self.org_id))
        self.etiqueta_regresar_buttom.grid(row=7, column=0, sticky="news", padx=20, pady=5)

    def verificar_datos(self):
        """
        Verifica los datos antes de guardar la entrada.
        Verifica si se ha seleccionado un mayor rango y si ya existe una dependencia de mayor rango en el organigrama.
        Verifica la longitud del nombre de la dependencia.
        Guarda la entrada.
        """
        if self.mayor_rango_selected.get():
            cursor.execute('SELECT COUNT(*) FROM dependencias WHERE DEPENDENCIA_PADRE_ID = 0 AND ORG_ID = ?',
                           (self.org_id,))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showinfo("Error",
                                    "Este organigrama ya posee una dependencia de mayor rango. Si quiere modificarla, regrese al apartado modificar.")
                return

        if self.verificar_longitud_nombre():
            return

        self.guardar_entry(self.ced)

    def mayor_rango(self):
        """
        Verifica si existe una dependencia de mayor rango en el organigrama.
        Si existe, muestra un mensaje de error y deselecciona la opción de mayor rango.
        Si no existe, guarda la entrada.
        """
        cursor.execute('SELECT COUNT(*) FROM dependencias WHERE DEPENDENCIA_PADRE_ID = 0 AND ORG_ID = ?',
                       (self.org_id,))
        print("ORG_ID EN MAYOR RANGO ES:", self.org_id)
        count = cursor.fetchone()[0]
        print("COUNT EN MAYOR RANGO", count)
        if count > 0:
            messagebox.showinfo("Error",
                                "Este organigrama ya posee una dependencia de mayor rango. Si quiere modificarla, regrese al apartado modificar.")
            self.mayor_rango_selected.set(False)
            self.additional_entry.set(False)
        else:
            self.guardar_entry(self.ced)

    def deshabilitar_checkbutton(self):
        """
        Deshabilita el checkbutton y oculta la entrada adicional si se selecciona la opción de mayor rango.
        Habilita el checkbutton si se deselecciona la opción de mayor rango.
        """
        if self.mayor_rango_selected.get():
            self.show_additional_entry.set(False)
            self.verificar_checkbutton.config(state='disabled')
            self.additional_entry_label.grid_remove()
            self.additional_entry.grid_remove()
        else:
            self.verificar_checkbutton.config(state='normal')

    def verificar_longitud_nombre(self):
        """
        Verifica la longitud del nombre de la dependencia.
        Si la longitud es menor a 1 o mayor a 25, muestra un mensaje de error.
        Devuelve True si la verificación falla para evitar guardar la entrada, False si la verificación es exitosa.
        """
        nombre = self.nombre_entry.get()
        if len(nombre) < 1 or len(nombre) > 25:
            messagebox.showerror("Error", "El nombre de la dependencia debe tener entre 1 y 25 caracteres.")
            return True  # Devuelve True si la verificación falla para evitar guardar la entrada

        return False  # Devuelve False si la verificación es exitosa

    def mostrar_error(self, mensaje):
        """
        Muestra un mensaje de error.
        Recibe el mensaje de error como parámetro.
        """
        messagebox.showerror("Error", mensaje)

    def guardar_entry(self, ced):
        """
        Guarda la entrada del formulario en la base de datos.
        Obtiene los valores ingresados en los campos de entrada.
        Realiza verificaciones y muestra mensajes de error en caso de incumplimiento de condiciones.
        Actualiza la lista de dependencias y los valores de la lista desplegable.
        Inserta los valores en la base de datos y muestra un mensaje de éxito.
        Limpia los campos de entrada y oculta la lista desplegable adicional.
        """
        CED = ced.get().title()
        NOM = self.nom.get().title()

        if self.show_additional_entry.get() and self.mayor_rango_selected.get():
            messagebox.showinfo("Error", "No se puede seleccionar ambas opciones de verificación.")
            return

        if not self.show_additional_entry.get() and not self.mayor_rango_selected.get():
            cursor.execute('SELECT COUNT(*) FROM dependencias WHERE DEPENDENCIA_PADRE_ID IS NULL AND ORG_ID = ?',
                           (self.org_id,))
            count = cursor.fetchone()[0]
            if count >= 5:
                messagebox.showinfo("Límite alcanzado", "Has llegado al límite (5) de dependencias sin asociar.")
                return

        if self.show_additional_entry.get():
            cursor.execute('SELECT ID FROM dependencias WHERE NOMBRE = ?', (NOM,))
            result = cursor.fetchone()
            if result:
                DEPENDENCIA_PADRE_ID = result[0]
                cursor.execute('SELECT COUNT(*) FROM dependencias WHERE DEPENDENCIA_PADRE_ID = ?',
                               (DEPENDENCIA_PADRE_ID,))
                count = cursor.fetchone()[0]
                if count >= 5:
                    messagebox.showinfo("Límite alcanzado",
                                        f"Has llegado al límite (5) de subdependencias asociadas a la dependencia {NOM}.")
                    return
            else:
                mensaje = "La dependencia asociada no existe."
                self.mostrar_error(mensaje)
                return
        else:
            DEPENDENCIA_PADRE_ID = None

        if self.mayor_rango_selected.get():
            DEPENDENCIA_PADRE_ID = 0

        # Quitar la verificación del botón de verificación
        self.show_additional_entry.set(False)
        self.mayor_rango_selected.set(False)
        self.verificar_checkbutton.config(state='normal')

        #Quitar la verificacion del boton de verificacion
        self.show_additional_entry.set(False)

        # Actualizar la lista de dependencias
        self.actualizar_lista_dependencias()

        # Actualizar los valores de la lista desplegable
        self.additional_entry['values'] = self.lista_dependencias

        # Mostrar la lista actualizada en la interfaz
        self.additional_entry_label.grid(row=2, column=5, sticky="e")
        self.additional_entry.grid(row=2, column=8, sticky="e")

        # Insertar los valores en la base de datos
        print(f"EL VALOR QUE SE ESTA QUERIENDO INGRESAR AQUI ES: {self.org_id}")
        cursor.execute('INSERT INTO dependencias (NOMBRE, DEPENDENCIA_PADRE_ID, ORG_ID) VALUES (?, ?, ?)',
                       (CED, DEPENDENCIA_PADRE_ID, self.org_id))
        conexion.commit()
        self.additional_entry_label.grid_remove()
        self.additional_entry.grid_remove()
        mensaje = "El departamento se ha insertado correctamente."
        messagebox.showinfo("Información", mensaje)
        self.additional_entry_label.grid_remove()
        self.additional_entry.grid_remove()
        self.ced.set("")
        self.nom.set("")

    def actualizar_lista_dependencias(self):
        """
        Actualiza la lista de dependencias en función de el organigrama actual.
        Obtiene la lista actualizada de dependencias desde la base de datos,
        filtrando por el ID de el organigrama actual.
        Actualiza el atributo "lista_dependencias" con los nombres de las dependencias obtenidas.
        Oculta la etiqueta y la entrada de texto adicionales si estaban visibles anteriormente.
        """
        # Obtener la lista actualizada de dependencias desde la base de datos
        cursor.execute('SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        self.lista_dependencias = [row[0] for row in cursor.fetchall()]
        self.additional_entry_label.grid_remove()
        self.additional_entry.grid_remove()

    def mostrar_entrada_adicional(self):
        """
        Muestra u oculta la etiqueta y la entrada de texto adicionales en función del estado del checkbox.
        Si el checkbox de entrada adicional está marcado, se muestra la etiqueta y la entrada de texto adicionales.
        Si el checkbox está desmarcado, se oculta la etiqueta y la entrada de texto adicionales.
        """
        if self.show_additional_entry.get():
            self.additional_entry_label.grid()
            self.additional_entry.grid()
        else:
            self.additional_entry_label.grid_remove()
            self.additional_entry.grid_remove()

        self.mainloop()  # esta linea sirve para que la ventana principal se siga viendo hasta que cerremos

    def regresar_entry(self, org_id):
        """
        Destruye la ventana actual y muestra la ventana "Agregar_y_modificar_dependencias".
        Recibe como parámetro el ID de el organigrama.
        Cierra la ventana actual y abre la ventana "Agregar_y_modificar_dependencias" con el ID de el organigrama recibido.
        """
        self.destroy()
        Agregar_y_modificar_dependencias(org_id)

    # ==================================================================================================================
    # ===================================INTERFAZ MODIFICAR LA DEPENDENCIA==============================================
    # ==================================================================================================================

    def crear_interfaz_modificar(self):
        """
        Crea la interfaz gráfica para la modificación de dependencias.

        - Obtiene la lista de dependencias existentes con el mismo ID_ORG.
        - Verifica si hay dependencias disponibles para modificar.
        - Configura el tamaño y título de la ventana principal.
        - Crea y configura el frame principal de la interfaz.
        - Configura variables para los campos de entrada.
        - Crea y configura el frame de información de la dependencia.
        - Configura y muestra el OptionMenu y ComboBox para seleccionar la dependencia a modificar.
        - Configura y muestra los campos de entrada para la información de la dependencia.
        - Crea y configura los campos de entrada para las subdependencias.
        - Crea y configura los botones de aceptar y regresar.
        - Mantiene la ventana principal abierta.
        """

        # Obtener lista de dependencias existentes con el mismo ID_ORG
        cursor.execute('SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        if not lista_dependencias:
            messagebox.showinfo("Información", "No hay elementos para modificar. Por favor, vaya a la sección de agregar.")
            return


        self.geometry("600x450")
        self.title("Modificar")  # Definimos el titulo del cuadro pirncipal


        self.frame = tk.Frame(self,  bd=4, relief="groove")

        self.frame.grid(row=0, column=0)
        colorFondo2 = "#FF2525"
        self.frame.config(bg=colorFondo2)


        self.ced = StringVar()
        self.nom = StringVar()
        self.ape = StringVar()
        self.tel = StringVar()
        self.dir = StringVar()
        self.dep = StringVar()
        self.sal = StringVar()
        self.nac = StringVar()
        self.puesto = StringVar()
        self.ced_buscar = StringVar()
        self.tamanho_de_letra = Font(size=15)  # tamaño de letra general"



        self.user_info_frame = tk.LabelFrame(self.frame, text="Informacion de la dependencia",font=self.tamanho_de_letra,bd=0, relief="groove")
        self.user_info_frame.grid(row=0, column=0, padx=40, pady=20)
        self.user_info_frame.config(bg=colorFondo2)

        self.ced_buscar.set("Nombre de la dependencia")
        # Obtener lista de dependencias existentes con el mismo ID_ORG
        cursor.execute('SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.dependencias_entry = tk.StringVar()
        self.dependencias_optionmenu = tk.OptionMenu(self.user_info_frame, self.dep, *lista_dependencias)

        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.departamento_entry.grid(row=0, column=1, padx=15, pady=10, columnspan=4)

        self.aceptar_button = tk.Button(self.user_info_frame, text="Aceptar",bg="white", fg="black", font=("Arial", 9, "bold"),width=10,command=self.validar_dependencia)
        self.aceptar_button.grid(row=0, column=0, padx=5, pady=10)

        self.cedula_label = tk.Label(self.user_info_frame, text="Nombre",bg=colorFondo2)
        self.cedula_label.grid(row=1, column=0)
        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.cedula_entry.grid(row=2, column=0)

        self.subdpendencias_label = tk.Label(self.user_info_frame, text="Subdependencias",bg=colorFondo2)
        self.subdpendencias_label.grid(row=1, column=1)

        # Crear las entries para las dependencias hijas
        self.entries = []
        for i in range(5):
            entry = tk.Entry(self.user_info_frame, textvariable=tk.StringVar())
            entry.grid(row=i + 2, column=1,pady=3)
            self.entries.append(entry)

        # Botom de agregar
        self.etiqueta_agregar_buttom = tk.Button(self.frame, text="CAMBIAR",bg="white", fg="black", font=("Arial", 9, "bold") ,command=self.validar_y_cambiar)
        self.etiqueta_agregar_buttom.grid(row=7, column=0, sticky="news", padx=20, pady=1)

        self.etiqueta_regresar_buttom = tk.Button(self.frame, text="REGRESAR",bg="white", fg="black", font=("Arial", 9, "bold"),
                                                  command=lambda: self.regresar_entry(self.org_id))
        self.etiqueta_regresar_buttom.grid(row=8, column=0, sticky="news", padx=20, pady=3)

        self.mainloop()  # esta linea sirve para que la ventana principal se siga viendo hasta que cerremos

    def cambiar_dependencias_hijas(self):
        """
        Actualiza las dependencias hijas en la base de datos.
        Obtiene las dependencias hijas ingresadas por el usuario.
        Actualiza los registros de dependencias hijas en la base de datos.
        """
        dependencias_hijas = [entry.get() for entry in self.entries]

        for i, dependencia_hija in enumerate(dependencias_hijas):
            if dependencia_hija:
                cursor.execute('UPDATE dependencias SET NOMBRE = ? WHERE DEPENDENCIA_PADRE_ID = ?',
                               (dependencia_hija, self.dependencia_id))
                conexion.commit()

    def validar_y_cambiar(self):
        """
        Valida y realiza el cambio de dependencias.
        Verifica si se han ingresado dependencias hijas válidas.
        Muestra un mensaje de error si no se han ingresado dependencias hijas válidas.
        Realiza el cambio de las dependencias.
        """
        dependencias_hijas = [entry.get() for entry in self.entries]
        tiene_dependencia_valida = False

        for dependencia_hija in dependencias_hijas:
            if len(dependencia_hija) > 0 and len(dependencia_hija) <= 50:
                tiene_dependencia_valida = True
                break

        if not tiene_dependencia_valida:
            messagebox.showerror("Error", "Agregue al menos una dependencia hija.")
            return

        self.cambiar_entry()


    def validar_dependencia(self):
        """
        Valida la dependencia seleccionada por el usuario.
        Obtiene el nombre de la dependencia seleccionada.
        Muestra el nombre de la dependencia en el campo de entrada correspondiente.
        Busca el ID de la dependencia seleccionada en la base de datos.
        Si se encuentra el ID, almacena el valor en self.dependencia_id.
        Si no se encuentra el ID, establece self.dependencia_id como None.
        """
        dependencia = self.dep.get()
        if dependencia:
            # Mostrar nombre de la empresa en el entry "Nombre"
            self.cedula_entry.delete(0, tk.END)
            self.cedula_entry.insert(tk.END, dependencia)

            # Buscar ID de la dependencia seleccionada
            cursor.execute('SELECT ID FROM dependencias WHERE NOMBRE = ? AND ORG_ID = ?', (dependencia, self.org_id))
            resultado = cursor.fetchone()
            print(resultado)
            if resultado:
                self.dependencia_id = resultado[0]
                # Utiliza el valor de 'dependencia_id' como necesites
                print("ID de la dependencia seleccionada:", self.dependencia_id)

                # Obtener dependencias hijas
                self.obtener_dependencias_hijas()
            else:
                self.dependencia_id = None
                print("No se encontró el ID de la dependencia")
        else:
            messagebox.showerror("Error", "Por favor, seleccione una dependencia.")

    def obtener_dependencias_hijas(self):
        """
        Obtiene las dependencias hijas de la dependencia seleccionada.
        Consulta la base de datos para obtener las dependencias hijas de la dependencia seleccionada.
        Almacena las dependencias hijas en self.dependencias_hijas.
        Actualiza los campos de entrada con los nombres de las dependencias hijas.
        """
        cursor.execute('SELECT ID, NOMBRE FROM dependencias WHERE DEPENDENCIA_PADRE_ID = ? AND ORG_ID = ?',
                       (self.dependencia_id, self.org_id))
        dependencias_hijas = cursor.fetchall()
        self.dependencias_hijas = dependencias_hijas
        print("Dependencias hijas:", self.dependencias_hijas)

        # Imprimir dependencias hijas en entries
        for i in range(5):
            if i < len(self.dependencias_hijas):
                entry = self.entries[i]
                entry.delete(0, tk.END)
                entry.insert(tk.END, self.dependencias_hijas[i][1])  # Nombre de la dependencia
            else:
                entry = self.entries[i]
                entry.delete(0, tk.END)

    def cambiar_entry(self):
        """
        Realiza el cambio de los nombres de las dependencias.
        Obtiene el nuevo valor para la dependencia padre.
        Obtiene las dependencias hijas ingresadas por el usuario.
        Verifica si las dependencias hijas tienen una longitud válida.
        Actualiza el nombre de la dependencia padre en la base de datos.
        Actualiza los nombres de las dependencias hijas en la base de datos.
        Muestra un mensaje de éxito.
        """
        nuevo_valor = self.cedula_entry.get()
        dependencias_hijas = [entry.get() for entry in self.entries if entry.get()]
        for dependencia_hija in dependencias_hijas:
            if len(dependencia_hija) > 50:
                messagebox.showerror("Error", "La longitud de las dependencias hijas debe ser menor a 50.")
                return

        print(nuevo_valor)
        print(self.dependencia_id)

        if self.dependencia_id and nuevo_valor:
            cursor.execute('UPDATE dependencias SET NOMBRE = ? WHERE ID = ?', (nuevo_valor, self.dependencia_id))
            conexion.commit()
            print("Nombre cambiado correctamente")

            # Actualizar los nombres de las dependencias hijas en la base de datos
            for i in range(len(self.dependencias_hijas)):
                nueva_dependencia_nombre = self.entries[i].get()
                nueva_dependencia_id = self.dependencias_hijas[i][0]  # ID de la dependencia hija
                cursor.execute('UPDATE dependencias SET NOMBRE = ? WHERE ID = ?',
                               (nueva_dependencia_nombre, nueva_dependencia_id))
                conexion.commit()
                print(f"Nombre de dependencia hija {i + 1} cambiado correctamente")

            messagebox.showinfo("Éxito", "Se han cambiado correctamente los nombres de las dependencias.")

        else:
            messagebox.showerror("Error", "Por favor, ingrese un nombre y un nuevo valor.")

    def mostrar_ventana_cambiado_correctamente(self):
        """
        Muestra una ventana indicando que los atributos se han modificado correctamente.
        Limpia los valores de las variables de control ced y nom.
        Crea nuevos Entry widgets con las variables de control actualizadas.
        Muestra un mensaje de información indicando que se han realizado los cambios correctamente.
        """
        self.ced.set("")
        self.nom.set("")

        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)

        messagebox.showinfo("CORRECTO", "Se modifico los atributos correctamente.")

    def buscar_persona(self, ced):
        """
        Busca una persona en la base de datos utilizando la cédula especificada.
        Obtiene el valor de la variable de control ced.
        Consulta la base de datos para obtener el nombre y la dependencia de la persona.
        Si se encuentra un resultado, actualiza las variables de control ced y nom.
        """
        aux = ced.get()
        CED = self.ced_buscar.get()
        cursor.execute('SELECT NOMBRE, DEPENDENCIA_PADRE_ID', (CED,))
        resultado = cursor.fetchone()
        if resultado:
            self.ced.set(resultado[0])
            self.nom.set(resultado[1])

    def mostrar_ventana_error(self):
        """
        Muestra una ventana de error indicando que no se encontró la dependencia.
        Muestra un mensaje de error indicando que no se encontró la dependencia.
        Crea nuevos Entry widgets con las variables de control ced y nom.
        """
        messagebox.showerror("Error", "No se encontró la dependencia.")
        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)

        messagebox.showerror("Error", "No se encontró la dependencia.")

    def regresar_entry_modificar(self, org_id):
        """
        Regresa a la ventana anterior después de modificar una dependencia.
        Destruye la ventana actual.
        Crea una nueva instancia de la ventana Agregar_y_modificar_dependencias con el ID de el organigrama.
        """
        self.destroy()
        Agregar_y_modificar_dependencias(org_id)

    # ==================================================================================================================
    # ===================================INTERFAZ DE ELIMINAR LA DEPENDENCIA============================================
    # ==================================================================================================================

    def crear_interfaz_eliminar(self):
        """
        Crea la interfaz gráfica para eliminar una dependencia.

        Obtiene la lista de dependencias existentes con el mismo ID_ORG.
        Si no hay dependencias, muestra un mensaje informativo y retorna.
        Configura el tamaño y título de la ventana.
        Crea un frame y lo coloca en la posición (0, 0).
        Configura el color de fondo del frame.
        Inicializa variables para los campos de entrada.
        Crea un label frame para mostrar la información de eliminación de una dependencia.
        Configura el color de fondo del label frame.
        Obtiene la lista de dependencias existentes con el mismo ID_ORG.
        Configura una variable de cadena con el nombre de la dependencia seleccionada.
        Crea un OptionMenu para seleccionar la dependencia a eliminar.
        Crea un Combobox para seleccionar la dependencia a eliminar.
        Crea un botón para aceptar la selección.
        Crea una etiqueta para mostrar el nombre de la dependencia seleccionada.
        Crea etiquetas para mostrar las subdependencias.
        Crea un botón para eliminar la dependencia seleccionada.
        Crea un botón para regresar.
        Ejecuta el bucle principal de la ventana.
        """
        # Obtener lista de dependencias existentes con el mismo ID_ORG
        cursor.execute('SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        if not lista_dependencias:
            messagebox.showinfo("Información", "No hay elementos para eliminar. Por favor, vaya a la sección de agregar.")
            return


        self.geometry("600x450")
        self.title("Eliminar")

        self.frame = tk.Frame(self,  bd=4, relief="groove")
        self.frame.grid(row=0, column=0)
        colorFondo3 = "#FF2525"
        self.frame.config(bg=colorFondo3)


        self.ced = StringVar()
        self.nom = StringVar()
        self.ape = StringVar()
        self.tel = StringVar()
        self.dir = StringVar()
        self.dep = StringVar()
        self.sal = StringVar()
        self.nac = StringVar()
        self.hijos = StringVar()
        self.ced_buscar = StringVar()
        self.tamanho_de_letra = Font(size=15)  # tamaño de letra general"


        self.user_info_frame = tk.LabelFrame(self.frame, text="Eliminar una dependencia",font=self.tamanho_de_letra,bd=0, relief="groove")
        self.user_info_frame.grid(row=0, column=0, padx=50, pady=20)
        self.user_info_frame.config(bg=colorFondo3)

        # Obtener lista de dependencias existentes con el mismo ID_ORG
        cursor.execute('SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.ced_buscar.set("Nombre de la dependencia")
        self.dependencias_entry = tk.StringVar()
        self.dependencias_optionmenu = tk.OptionMenu(self.user_info_frame, self.dep, *lista_dependencias)


        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.departamento_entry.grid(row=0, column=1, padx=15, pady=10, columnspan=4)

        self.aceptar_button = tk.Button(self.user_info_frame, text="Aceptar",bg="white", font=("Arial", 9, "bold"),
                                        command=self.validar_dependencia_aeliminar)
        self.aceptar_button.grid(row=0, column=0, padx=5, pady=10)

        self.cedula_label = tk.Label(self.user_info_frame, text="Nombre",bg=colorFondo3)
        self.cedula_label.grid(row=1, column=0)
        self.cedula_entry = tk.Label(self.user_info_frame, textvariable=self.ced,bg=colorFondo3)
        self.cedula_entry.grid(row=2, column=0)

        self.subdpendencias_label = tk.Label(self.user_info_frame, text="Subdependencias",bg=colorFondo3)
        self.subdpendencias_label.grid(row=1, column=1)

        # Crear las etiquetas para las dependencias hijas
        self.labels = []
        for i in range(5):
            label = tk.Label(self.user_info_frame, text="",bg=colorFondo3)
            label.grid(row=i + 2, column=1)
            self.labels.append(label)

        # Boton de agregar
        self.etiqueta_agregar_buttom = tk.Button(self.frame, text="ELIMINAR",fg="black",bg="white", font=("Arial", 9, "bold"),
                                                 command=lambda: self.eliminar_entry())
        self.etiqueta_agregar_buttom.grid(row=7, column=0, sticky="news", padx=20, pady=1)

        self.etiqueta_regresar_buttom = tk.Button(self.frame, text="REGRESAR",fg="black", bg="white", font=("Arial", 9, "bold"),
                                                  command=lambda: self.regresar_entry(self.org_id))
        self.etiqueta_regresar_buttom.grid(row=8, column=0, sticky="news", padx=20, pady=1)

        self.mainloop()  # esta linea sirve para que la ventana principal se siga viendo hasta que cerremos

    def validar_dependencia_aeliminar(self):
        """
        Valida la dependencia a eliminar seleccionada por el usuario.

        Obtiene la dependencia seleccionada y muestra su nombre en una etiqueta.
        Busca el ID de la dependencia seleccionada en la base de datos.
        Si se encuentra el ID, guarda el ID de la dependencia y obtiene sus dependencias hijas.
        Limpia las etiquetas anteriores y muestra las dependencias hijas en las etiquetas correspondientes.
        """
        dependencia = self.dep.get()
        if dependencia:
            # Mostrar nombre de la empresa en el label "Nombre"
            self.ced.set(dependencia)

            # Buscar ID de la dependencia seleccionada
            cursor.execute('SELECT ID FROM dependencias WHERE NOMBRE = ? AND ORG_ID = ?', (dependencia, self.org_id))
            resultado = cursor.fetchone()
            if resultado:
                dependencia_id = resultado[0]
                print("ID de la dependencia seleccionada:", dependencia_id)
                self.dependencia_id = dependencia_id

                # Limpiar las líneas de texto anteriores
                for label in self.labels:
                    label.config(text="")

                # Obtener dependencias hijas
                self.obtener_dependencias_hijas_aeliminar()

            else:
                print("No se encontró el ID de la dependencia")
        else:
            messagebox.showerror("Error", "Por favor, seleccione una dependencia.")

    def obtener_dependencias_hijas_aeliminar(self):
        """
        Obtiene las dependencias hijas de la dependencia a eliminar.

        Busca en la base de datos las dependencias que tengan como dependencia padre el ID de la dependencia seleccionada.
        Guarda las dependencias hijas en una variable de instancia.
        Muestra los nombres de las dependencias hijas en las etiquetas correspondientes.
        """
        cursor.execute('SELECT ID, NOMBRE FROM dependencias WHERE DEPENDENCIA_PADRE_ID = ? AND ORG_ID = ?',
                       (self.dependencia_id, self.org_id))
        dependencias_hijas = cursor.fetchall()
        self.dependencias_hijas = dependencias_hijas
        print("Dependencias hijas:", self.dependencias_hijas)

        # Mostrar dependencias hijas en las etiquetas correspondientes
        for i, dependencia_hija_id in enumerate(self.dependencias_hijas):
            nombre_hija = self.dependencias_hijas[i][1]  # Obtener nombre de la dependencia hija
            self.labels[i].config(text=f"{nombre_hija}")


    def eliminar_entry(self):
        """
        Elimina la dependencia seleccionada y sus dependencias hijas de la base de datos.
        Recibe el ID de la dependencia a eliminar.
        Ejecuta una consulta para eliminar la dependencia y sus dependencias hijas.
        Muestra un mensaje de confirmación y realiza otras acciones necesarias después de la eliminación.
        """
        # Eliminar la dependencia seleccionada y sus dependencias hijas
        cursor.execute('DELETE FROM dependencias WHERE ID = ? OR DEPENDENCIA_PADRE_ID = ?',
                       (self.dependencia_id, self.dependencia_id))
        conexion.commit()
        print("Dependencia eliminada correctamente")

        # Mostrar mensaje de confirmación
        messagebox.showinfo("Eliminación exitosa", "Se ha eliminado correctamente las dependencias seleccionadas")

    def confirmar_eliminar(self):
        """
        Realiza la confirmación y eliminación de una dependencia y sus subdependencias.
        Obtiene la dependencia seleccionada.
        Muestra un mensaje de confirmación para eliminar la dependencia y sus subdependencias.
        Si el usuario confirma la eliminación, busca el ID de la dependencia seleccionada en la base de datos.
        Si se encuentra el ID, elimina la dependencia y sus subdependencias llamando al método eliminar_dependencias.
        Imprime un mensaje indicando que se ha eliminado correctamente.
        Si no se encuentra el ID de la dependencia, imprime un mensaje de error.
        Si no se selecciona ninguna dependencia, muestra un mensaje de error.
        """
        # Obtener la dependencia seleccionada
        dependencia = self.dep.get()
        if dependencia:
            # Mostrar un mensaje de confirmación
            respuesta = messagebox.askyesno("Confirmar eliminación",
                                            f"¿Estás seguro que quieres eliminar la dependencia '{dependencia}' y sus subdependencias?")

            if respuesta:
                # Buscar ID de la dependencia seleccionada
                cursor.execute('SELECT ID FROM dependencias WHERE NOMBRE = ? AND ORG_ID = ?',
                               (dependencia, self.org_id))
                resultado = cursor.fetchone()
                if resultado:
                    dependencia_id = resultado[0]
                    # Eliminar la dependencia y sus subdependencias
                    self.eliminar_dependencias(dependencia_id)
                    print("Se ha eliminado correctamente las dependencias seleccionadas")
                else:
                    print("No se encontró el ID de la dependencia")
            else:
                print("Eliminación cancelada por el usuario")
        else:
            messagebox.showerror("Error", "Por favor, seleccione una dependencia.")

    def eliminar_dependencias(self, dependencia_id):
        """
        Elimina una dependencia y sus subdependencias de la base de datos.
        Recibe el ID de la dependencia a eliminar.
        Ejecuta una consulta para eliminar la dependencia y sus subdependencias en la base de datos.
        Realiza la confirmación de los cambios en la base de datos.
        """
        # Eliminar la dependencia y sus subdependencias
        cursor.execute('DELETE FROM dependencias WHERE ID = ? OR DEPENDENCIA_PADRE_ID = ?',
                       (dependencia_id, dependencia_id))
        conexion.commit()

    def regresar_entry_eliminar(self):
        """
        Destruye la ventana actual y vuelve a la ventana de Agregar_y_modificar_dependencias.
        Cierra la ventana actual.
        Crea una nueva instancia de la ventana Agregar_y_modificar_dependencias y la muestra.
        """
        self.destroy()
        Agregar_y_modificar_dependencias(self.org_id)

    # ==================================================================================================================
    # ===================================INTERFAZ DE MOVER LA DEPENDENCIA===============================================
    # ==================================================================================================================

    def crear_interfaz_mover(self):
        """
        Crea la interfaz para mover dependencias.

        - Obtiene la lista de dependencias existentes con el mismo ID_ORG.
        - Si no hay dependencias, muestra un mensaje informativo y retorna.
        - Configura la geometría y título de la ventana.
        - Crea un marco (frame) en la ventana.
        - Configura el estilo y tamaño del marco.
        - Configura variables de control y opciones de entrada.
        - Crea un marco de información de usuario.
        - Obtiene la lista de dependencias existentes para la selección de la dependencia a mover.
        - Configura un botón de aceptar.
        - Crea etiquetas y entradas de texto para mostrar información de la dependencia seleccionada.
        - Obtiene la lista de dependencias existentes para la dependencia a la que se va a asociar.
        - Crea etiquetas y entradas de texto para las subdependencias.
        - Crea botones para mover y regresar.
        - Ejecuta el bucle principal de la ventana.
        """
        # Obtener lista de dependencias existentes con el mismo ID_ORG
        cursor.execute('SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        if not lista_dependencias:
            messagebox.showinfo("Información", "No hay elementos para mover. Por favor, vaya a la sección de agregar.")
            return


        self.geometry("600x450")
        self.title("Editar ubicación de dependencias")

        self.frame = tk.Frame(self,  bd=4, relief="groove")
        self.frame.grid(row=0, column=0)
        colorFondo3 = "#FF2525"
        self.frame.config(bg=colorFondo3)


        self.ced = StringVar()
        self.nom = StringVar()
        self.ape = StringVar()
        self.tel = StringVar()
        self.dir = StringVar()
        self.dep = StringVar()
        self.sal = StringVar()
        self.nac = StringVar()
        self.hijos = StringVar()
        self.ced_buscar = StringVar()
        self.tamanho_de_letra = Font(size=15)  # tamaño de letra general"


        self.user_info_frame = tk.LabelFrame(self.frame, text="Editar ubicación de dependencias",font=self.tamanho_de_letra,bd=0, relief="groove")
        self.user_info_frame.grid(row=0, column=0, padx=50, pady=20)
        self.user_info_frame.config(bg=colorFondo3)

        # Obtener lista de dependencias existentes con el mismo ID_ORG para la seleccion de dependencia a mover de lugar
        cursor.execute('SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]
        print("Lista de dependencias ascciadas a este organigrama:", lista_dependencias)

        self.ced_buscar.set("Nombre de la dependencia")
        self.dependencias_entry = tk.StringVar()
        self.dependencias_optionmenu = tk.OptionMenu(self.user_info_frame, self.dep, *lista_dependencias)


        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.departamento_entry.grid(row=0, column=1, padx=15, pady=10, columnspan=4)

        self.aceptar_button = tk.Button(self.user_info_frame, text="Aceptar",bg="white", font=("Arial", 9, "bold"),
                                        command=self.validar_dependencia_aeliminar)
        self.aceptar_button.grid(row=0, column=0, padx=5, pady=10)

        self.nombre_label = tk.Label(self.user_info_frame, text="Nombre",bg=colorFondo3)
        self.nombre_label.grid(row=1, column=0)
        self.nombre_entry = tk.Label(self.user_info_frame, textvariable=self.ced,bg=colorFondo3)
        self.nombre_entry.grid(row=2, column=0)

        self.subdpendencias_label = tk.Label(self.user_info_frame, text="Subdependencias",bg=colorFondo3)
        self.subdpendencias_label.grid(row=1, column=1)



        # Obtener lista de dependencias existentes con el mismo ID_ORG para la dependencia a la que se va a asociar
        cursor.execute('SELECT NOMBRE FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias_asociar = [row[0] for row in cursor.fetchall()]

        self.texto_label = tk.Label(self.user_info_frame, text="Estará asociada a:", bg=colorFondo3)
        self.texto_label.grid(row=7, column=0, sticky="e", pady=5)
        self.departamento2_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias_asociar)
        self.departamento2_entry.grid(row=7, column=1, padx=15, pady=10, columnspan=4)

        # Crear las etiquetas para las dependencias hijas
        self.labels = []
        for i in range(5):
            label = tk.Label(self.user_info_frame, text="",bg=colorFondo3)
            label.grid(row=i + 2, column=1)
            self.labels.append(label)

        # Boton de agregar
        self.etiqueta_agregar_buttom = tk.Button(self.frame, text="MOVER",fg="black",bg="white", font=("Arial", 9, "bold"),
                                                 command=lambda: self.mover_entry())
        self.etiqueta_agregar_buttom.grid(row=7, column=0, sticky="news", padx=20, pady=1)

        self.etiqueta_regresar_buttom = tk.Button(self.frame, text="REGRESAR",fg="black", bg="white", font=("Arial", 9, "bold"),
                                                  command=lambda: self.regresar_entry(self.org_id))
        self.etiqueta_regresar_buttom.grid(row=8, column=0, sticky="news", padx=20, pady=1)

        self.mainloop()  # esta linea sirve para que la ventana principal se siga viendo hasta que cerremos


    def regresar_entry_mover(self):
        """
        Regresa a la interfaz de agregar y modificar dependencias.
        Destruye la ventana actual y muestra la interfaz Agregar_y_modificar_dependencias.
        """
        self.destroy()
        Agregar_y_modificar_dependencias(self.org_id)

    def mover_entry(self):
        """
        Mueve una dependencia a una nueva dependencia padre.
        Obtiene el nombre de la dependencia y el nombre de la nueva dependencia padre ingresados por el usuario.
        Verifica que la dependencia seleccionada no sea igual a la nueva dependencia padre.
        Consulta la base de datos para obtener el ID y el ID_DEPENDENCIA_PADRE de la dependencia que se va a mover.
        Verifica si la dependencia seleccionada es la raíz y si se puede reubicar debajo de la nueva dependencia padre.
        Obtiene el ID de la nueva dependencia padre.
        Verifica si la nueva dependencia padre tiene menos de 5 dependencias hijas.
        Verifica si la nueva dependencia padre no es descendiente directo o indirecto de la dependencia que se mueve.
        Actualiza el DEPENDENCIA_PADRE_ID de la dependencia que se mueve.
        Muestra un mensaje de reubicación exitosa.
        """
        nombre_dependencia = self.departamento_entry.get()
        nombre_nueva_dependencia_padre = self.departamento2_entry.get()

        print("NOMBRE_DEPENDENCIA:", nombre_dependencia)
        print("NOMBRE_NUEVA_DEPENDENCIA_PADRE:", nombre_nueva_dependencia_padre)

        # Obtener el ID y el ID_DEPENDENCIA_PADRE de la dependencia que se va a mover
        cursor.execute('SELECT ID, DEPENDENCIA_PADRE_ID FROM dependencias WHERE ORG_ID = ? AND NOMBRE = ?',
                       (self.org_id, nombre_dependencia))
        resultado = cursor.fetchone()
        if resultado:
            dependencia_id, dependencia_padre_id = resultado

            # Verificar si la dependencia seleccionada no es igual a la nueva dependencia padre
            if nombre_dependencia != nombre_nueva_dependencia_padre:
                # Se verifica si la dependencia seleccionada es la raiz, porque si lo es entonces no se puede reubicar.
                cursor.execute('SELECT DEPENDENCIA_PADRE_ID FROM dependencias WHERE ORG_ID = ? AND NOMBRE = ?',
                               (self.org_id, nombre_dependencia))
                verificar_dependencia_raiz = cursor.fetchone()[0]
                print("VERIFICAR DEPENDENCIA RAIZ:", verificar_dependencia_raiz)

                if verificar_dependencia_raiz != 0:
                    #Si el ID extraido es diferente de 0, no se trata de la raiz y se procede a verificar los otros puntos
                    #para la reubicacion
                    # Obtener el ID de la dependencia padre a la que se quiere asociar la dependencia seleccionada
                    cursor.execute('SELECT ID FROM dependencias WHERE ORG_ID = ? AND NOMBRE = ?',
                                   (self.org_id, nombre_nueva_dependencia_padre))
                    print("NOMBRE DE LA DEPENDENCIA PADRE SELECCIONADA ANTES DE CONTAR DEPENDENCIAS HIJAS:",
                          nombre_nueva_dependencia_padre)
                    print("ORG_ID ANTES DE CONTAR LAS DEPENDENCIAS HIJAS:",
                          self.org_id)
                    id_nueva_dependencia_padre = cursor.fetchone()[0]
                    print("NUEVA DEPENDENCIA PADRE ID SELECCIONADA ANTES DE CONTAR DEPENDENCIAS HIJAS:", id_nueva_dependencia_padre)

                    # Verificar si la nueva dependencia padre tiene menos de 5 dependencias hijas
                    cursor.execute('SELECT COUNT(*) FROM dependencias WHERE ORG_ID = ? AND DEPENDENCIA_PADRE_ID = ?',
                                   (self.org_id, id_nueva_dependencia_padre))
                    cantidad_hijas = cursor.fetchone()[0]
                    print("CANTIDAD DE HIJOS DE LA DEPENDENCIA A LA QUE SE QUIERE MOVER:", cantidad_hijas)

                    if cantidad_hijas < 5:
                        # Verificar si la nueva dependencia padre no es descendiente directo o indirecto de la dependencia que se mueve
                        print("DEPENDENCIA_ID:", dependencia_id)
                        print("ID_NUEVA_DEPENDENCIA_PADRE:", id_nueva_dependencia_padre)
                        if not self.es_descendiente(dependencia_id, id_nueva_dependencia_padre):
                            # Verificar si la nueva dependencia padre tiene ID_DEPENDENCIA_PADRE igual a 0
                            cursor.execute(
                                'SELECT ID FROM dependencias WHERE ORG_ID = ? AND NOMBRE = ? AND DEPENDENCIA_PADRE_ID = 0',
                                (self.org_id, nombre_nueva_dependencia_padre))
                            dependencia_padre_raiz = cursor.fetchone()

                            if dependencia_padre_raiz:
                                print("SE HA SELECCIONADO MOVER LA DEPENDENCIA DEBAJO DE LA RAIZ.")
                                # Actualizar el DEPENDENCIA_PADRE_ID de la dependencia que se mueve a NULL
                                cursor.execute('UPDATE dependencias SET DEPENDENCIA_PADRE_ID = NULL WHERE ID = ?',
                                               (dependencia_id,))
                                conexion.commit()

                                messagebox.showinfo("Reubicación exitosa", "Se ha movido correctamente la dependencia.")
                            else:
                                # Obtener el ID de la nueva dependencia padre
                                cursor.execute('SELECT ID FROM dependencias WHERE ORG_ID = ? AND NOMBRE = ?',
                                               (self.org_id, nombre_nueva_dependencia_padre))
                                nueva_dependencia_padre_id = cursor.fetchone()[0]
                                print("NUEVA DEPENDENCIA PADRE ID SELECCIONADA:", nueva_dependencia_padre_id)

                                # Actualizar el DEPENDENCIA_PADRE_ID de la dependencia que se mueve
                                cursor.execute('UPDATE dependencias SET DEPENDENCIA_PADRE_ID = ? WHERE ID = ?',
                                               (nueva_dependencia_padre_id, dependencia_id))
                                conexion.commit()

                                messagebox.showinfo("Reubicación exitosa", "Se ha movido correctamente la dependencia.")
                        else:
                            messagebox.showerror("Error",
                                                 "La nueva dependencia padre no puede ser descendiente de la dependencia que se mueve.")
                    else:
                        messagebox.showerror("Error",
                                             "La nueva dependencia a la que se quiere asociar ya tiene 5 subdependencias. No se puede agregar más.")
                else:
                    messagebox.showerror("Error",
                                             "La dependencia que intenta mover no puede ser la dependencia de mando. Intente con otra dependencia.")
            else:
                messagebox.showerror("Error", "La dependencia no se puede asociar a si misma.")
        else:
            messagebox.showerror("Error", "No se encontró la dependencia en la base de datos.")

    def es_descendiente(self, dependencia_id, nueva_dependencia_padre_id):
        """
        Verifica si una nueva dependencia padre es descendiente directo o indirecto de la dependencia que se mueve.
        Recibe los identificadores de la dependencia que se mueve (dependencia_id) y la nueva dependencia padre
        (nueva_dependencia_padre_id).
        Imprime los identificadores de las dependencias para fines de depuración.
        Obtiene todas las dependencias descendientes directas de la dependencia que se intenta mover.
        Si la nueva dependencia padre se encuentra entre los descendientes directos, devuelve True.
        Si no se encuentra entre los descendientes directos, realiza una verificación recursiva para las dependencias
        descendientes indirectas.
        Si se encuentra entre los descendientes indirectos, devuelve True.
        Si no se encuentra en ninguna de las verificaciones, devuelve False.
        """
        # Verificar si la nueva dependencia padre es descendiente directo o indirecto de la dependencia que se mueve
        print("DEPENDENCIA ID: ", dependencia_id)
        print("NUEVA_DEPENDENCIA_PADRE_ID", nueva_dependencia_padre_id)

        # Obtener todas las dependencias descendientes directas de la dependencia que se intenta mover
        cursor.execute('SELECT ID FROM dependencias WHERE ORG_ID = ? AND DEPENDENCIA_PADRE_ID = ?',
                       (self.org_id, dependencia_id))
        descendientes = [row[0] for row in cursor.fetchall()]

        print("DESCENDIENTES DIRECTOS", descendientes)
        if nueva_dependencia_padre_id in descendientes:
            return True

        # Obtener todas las dependencias descendientes indirectas de la dependencia que se intenta mover
        for descendiente in descendientes:
            print("Descendiente en el ciclo for:", descendiente)
            print("dependencia_id en el ciclo for:", dependencia_id)
            if self.es_descendiente(descendiente,
                                    nueva_dependencia_padre_id):  # Corrección en los argumentos de la llamada recursiva
                print("DESCENDIENTES INDIRECTOS", descendientes)
                return True

        return False


def ejecutar_dependencias(org_id):
    """
    Ejecuta el proceso de agregar y modificar dependencias para un organigrama.
    Recibe el identificador del organigrama (org_id).
    Imprime el identificador de el organigrama para fines de depuración.
    Llama a la función Agregar_y_modificar_dependencias pasando el identificador de el organigrama como argumento.
    """
    print("org_id dentro de ejecutar_dependencias es:", org_id)
    Agregar_y_modificar_dependencias(org_id)




