import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter import *
from tkinter import messagebox
import sqlite3


conexion = sqlite3.connect('organigrama.db')
cursor = conexion.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS personas (ID INTEGER PRIMARY KEY, CED TEXT, NOM TEXT, APE TEXT, '
               'TEL TEXT, DIR TEXT, DEP TEXT, SAL TEXT, NAC TEXT, PUE TEXT, ORG_ID TEXT)')


class vincular(tk.Tk):
    def __init__(self, org_id):
        tk.Tk.__init__(self)

        self.title("Vincular")
        self.org_id = org_id
        print("ORF_ID ES:", org_id)
        self.geometry("600x450")
        self.config(bg="#FF2525")
        self.frame = tk.Frame(self)
        self.resizable(False, False)
        self.frame.grid(row=0, column=0)
        self.frame_botones_inferiores = tk.Frame(self)
        self.frame_botones_inferiores.grid(row=1, column=0)

        self.botones = tk.LabelFrame(self.frame,bg="#FF2525",bd=0, relief="groove")
        self.botones.grid(row=0, column=0)

        self.etiqueta_agregar_buttom = tk.Button(self.botones, text="AGREGAR",bg="white", fg="black", font=("Arial", 9, "bold") ,command=self.save)
        self.etiqueta_agregar_buttom.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)
        self.etiqueta_agregar_buttom.config(width=8, height=1)

        self.etiqueta_eliminar_buttom = tk.Button(self.botones, text="MODIFICAR",bg="white", fg="black", font=("Arial", 9, "bold") ,command=self.crear_interfaz_modificar)
        self.etiqueta_eliminar_buttom.grid(row=1, column=2, sticky="nsew", padx=10, pady=5)

        self.etiqueta_modificar_buttom = tk.Button(self.botones, text="ELIMINAR",bg="white", fg="black", font=("Arial", 9, "bold") ,command=self.crear_interfaz_eliminar)
        self.etiqueta_modificar_buttom.grid(row=2, column=2, sticky="nsew", padx=10, pady=5)

        self.regresar_vinculo = tk.Button(self.botones, text="REGRESAR",bg="white", fg="black", font=("Arial", 9, "bold") ,command=self.Regresar_A_Inicio)
        self.regresar_vinculo.grid(row=4, column=2, sticky="nsew", padx=10, pady=5)

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
        Busca el ID de usuario en la tabla "organigrama" utilizando el ID de organigrama como filtro.
        Realiza una consulta a la base de datos para obtener el ID de usuario asociado al ID de organigrama especificado.
        Si se encuentra un resultado, devuelve el ID de usuario.
        Si no se encuentra un resultado, devuelve None.
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
        Regresa a la ventana principal.
        Invoca el método "buscar_usuario_id" para obtener el ID de usuario asociado al ID de organigrama.
        Cierra la ventana actual.
        Crea una nueva instancia de la clase VentanaPrincipal y pasa el ID de usuario como argumento.
        Ejecuta el bucle principal de la ventana principal.
        """
        user_id = self.buscar_usuario_id()  # Invocar al método con paréntesis para obtener el resultado
        print("USUARIO ID EN REGRESAR A INICIO:", user_id)

        self.destroy()
        from HOME import VentanaPrincipal
        print("Se envía la ID DE USUARIO a la ventana principal:", user_id)
        VentanaPrincipal(user_id)
        VentanaPrincipal.mainloop(self)

    def save(self):
        """
        Configura el título y crea la interfaz para agregar.
        Establece el título del cuadro principal como "Agregar".
        Crea la interfaz gráfica para agregar.
        """
        self.title("Agregar")  # Definimos el titulo del cuadro pirncipal
        self.crear_interfaz_agregar()

    # ==================================================================================================================
    # ===================================INTERFAZ DE AGREGAR A UNA PERSONA==============================================
    # ==================================================================================================================

    def crear_interfaz_agregar(self):
        """
        Crea la interfaz gráfica para agregar información de un empleado.
        Configura variables de control para los campos de entrada.
        Crea un marco principal y lo coloca en la ventana principal.
        Configura el estilo y el fondo del marco principal.
        Crea un sub-marco para la información del empleado y lo coloca dentro del marco principal.
        Configura etiquetas y campos de entrada para la información del empleado.
        Obtiene la lista de dependencias existentes desde la base de datos.
        Crea etiquetas y campos de selección para el departamento y el puesto.
        Crea botones de agregar y regresar.
        Ejecuta el bucle principal para mostrar la interfaz gráfica.
        """
        self.ced = StringVar()
        self.nom = StringVar()
        self.ape = StringVar()
        self.tel = StringVar()
        self.dir = StringVar()
        self.dep = StringVar()
        self.sal = StringVar()
        self.nac = StringVar()
        self.puesto = StringVar()

        self.frame = tk.Frame(self,highlightbackground="white", highlightthickness=3)  # creamos un mini ventana dentro de la ventana principal
        self.frame.grid(row=0, column=0)
        self.tamanho_de_letra = Font(size=15)  # tamaño de letra general"
        colorFondo = "#FF2525"
        self.frame.config(bg=colorFondo)


        self.user_info_frame = tk.LabelFrame(self.frame, text="Informacion del empleado", font=self.tamanho_de_letra,bd=0, relief="groove")
        self.user_info_frame.grid(row=0, column=0, padx=20, pady=20)
        self.user_info_frame.config(bg=colorFondo)
        self.cedula_label = tk.Label(self.user_info_frame, text="Cédula",bg=colorFondo)
        self.cedula_label.grid(row=0, column=0,padx=1)
        self.name_label = tk.Label(self.user_info_frame, text="Nombres",bg=colorFondo)
        self.name_label.grid(row=0, column=1,padx=1)

        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.cedula_entry.grid(row=1, column=0,padx=1)

        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)
        self.nombre_entry.grid(row=1, column=1,padx=1)

        self.apellido_label = tk.Label(self.user_info_frame, text="Apellidos",bg=colorFondo)
        self.apellido_entry = tk.Entry(self.user_info_frame, textvariable=self.ape)
        self.apellido_label.grid(row=0, column=2,padx=1)
        self.apellido_entry.grid(row=1, column=2,padx=1)

        self.phone_label = tk.Label(self.user_info_frame, text="Telefono",bg=colorFondo)
        self.phone_label.grid(row=2, column=0,padx=1)
        self.phone_entry = tk.Entry(self.user_info_frame, textvariable=self.tel)
        self.phone_entry.grid(row=3, column=0,padx=1)

        self.nacionality_label = tk.Label(self.user_info_frame, text="Nacionalidad",bg=colorFondo)
        self.nacionality_label.grid(row=2, column=1,padx=1)
        self.nacionality_comboBox = ttk.Combobox(self.user_info_frame,
                                                 values=["Paraguay", "Brasil", "Perú", "Argentina"], textvariable=self.nac)
        self.nacionality_comboBox.grid(row=3, column=1,padx=1)

        self.sueldo_label = tk.Label(self.user_info_frame, text="Salario",bg=colorFondo)
        self.sueldo_label.grid(row=2, column=2,padx=1)
        self.sueldo_entry = tk.Entry(self.user_info_frame, textvariable=self.sal)
        self.sueldo_entry.grid(row=3, column=2,padx=1)

        self.direccion_label = tk.Label(self.user_info_frame, text="Dirección de vivienda",bg=colorFondo)
        self.direccion_entry = tk.Entry(self.user_info_frame, textvariable=self.dir)
        self.direccion_label.grid(row=4, column=0,padx=1)
        self.direccion_entry.grid(row=5, column=0,padx=1)

        # Obtener lista de dependencias existentes
        cursor.execute('SELECT nombre FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.departamento_label = tk.Label(self.user_info_frame, text="Departamento",bg=colorFondo)
        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.departamento_label.grid(row=4, column=1,padx=1)
        self.departamento_entry.grid(row=5, column=1,padx=1)

        self.puesto_label = tk.Label(self.user_info_frame, text="Puesto",bg=colorFondo)
        self.puesto_label.grid(row=4, column=2,padx=1)
        self.puesto_comboBox = ttk.Combobox(self.user_info_frame,
                                            values=["Empleado", "Jefe de Departamento", "Director Ejecutivo"], textvariable=self.puesto)
        self.puesto_comboBox.grid(row=5, column=2,padx=1)

        # Boton de agregar
        self.etiqueta_agregar_buttom = tk.Button(self.frame, text="AGREGAR",bg="white", fg="black", font=("Arial", 9, "bold") ,command=self.validar_y_guardar_entry)
        self.etiqueta_agregar_buttom.grid(row=6, column=0, sticky="news", padx=20, pady=1)

        self.etiqueta_regresar_buttom = tk.Button(self.frame, text="REGRESAR",bg="white", fg="black", font=("Arial", 9, "bold"),
                                                  command=lambda: self.regresar_entry())
        self.etiqueta_regresar_buttom.grid(row=7, column=0, sticky="news", padx=20, pady=5)

        self.mainloop()  # esta linea sirve para que la ventana principal se siga viendo hasta que cerremos

    def validar_y_guardar_entry(self):
        """
        Valida los campos de entrada y guarda la entrada si es válida.
        Realiza validaciones en diferentes campos de entrada, como cédula, nombre, apellido,
        teléfono, salario y dirección.
        Muestra mensajes de error si alguna validación no es satisfactoria.
        Si todas las validaciones son exitosas, guarda la entrada.
        """
        valid_entries = [
            (self.Validar_Cedula(), "La cédula debe tener entre 1 y 10 caracteres."),
            (self.Validar_Nombre_Apellido(), "El nombre y apellido deben tener entre 1 y 30 caracteres."),
            (self.Validar_Telefono(), "El teléfono debe tener entre 1 y 10 caracteres."),
            (self.Validar_Salario(), "El salario debe tener entre 1 y 10 caracteres."),
            (self.Validar_Direccion(), "La dirección de vivienda debe tener entre 1 y 50 caracteres.")
        ]

        error_messages = [message for valid, message in valid_entries if not valid]

        if error_messages:
            error_message = "\n".join(error_messages)
            messagebox.showerror("Error", error_message)
        else:
            self.guardar_entry(self.ced)

    def Validar_Cedula(self):
        """
        Valida el campo de entrada de la cédula.
        Verifica que la longitud de la cédula esté entre 1 y 10 caracteres.
        Devuelve True si la validación es exitosa, False de lo contrario.
        """
        cedula = self.cedula_entry.get()
        if len(cedula) > 0 and len(cedula) < 11:
            return True
        else:
            return False

    def Validar_Nombre_Apellido(self):
        """
        Valida los campos de entrada de nombre y apellido.
        Verifica que la longitud del nombre y apellido estén entre 1 y 30 caracteres.
        Devuelve True si la validación es exitosa, False de lo contrario.
        """
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        if (len(nombre) > 0 and len(nombre) < 31 ) and (len(apellido) > 0 and len(apellido) < 31):
            return True
        else:
            return False

    def Validar_Telefono(self):
        """
        Valida el campo de entrada de teléfono.
        Verifica que la longitud del teléfono esté entre 1 y 10 caracteres.
        Devuelve True si la validación es exitosa, False de lo contrario.
        """
        telefono = self.phone_entry.get()
        if len(telefono) > 0 and len(telefono) < 11:
            return True
        else:
            return False

    def Validar_Salario(self):
        """
        Valida el campo de entrada de salario.
        Verifica que la longitud del salario esté entre 1 y 10 caracteres.
        Devuelve True si la validación es exitosa, False de lo contrario.
        """
        salario = self.sueldo_entry.get()
        if len(salario) > 0 and len(salario) < 11:
            return True
        else:
            return False

    def Validar_Direccion(self):
        """
        Valida el campo de entrada de dirección.
        Verifica que la longitud de la dirección esté entre 1 y 50 caracteres.
        Devuelve True si la validación es exitosa, False de lo contrario.
        """

        direccion = self.direccion_entry.get()
        if len(direccion) > 0 and len(direccion) < 51:
            return True
        else:
            return False


    def guardar_entry(self, ced):
        """
        Guarda los datos ingresados en los campos de entrada en la base de datos.
        Obtiene los valores de los campos de entrada.
        Inserta los valores en la base de datos mediante una consulta SQL.
        Imprime los valores de los campos en la consola para verificar su contenido.
        Limpia los campos de entrada.
        Muestra un mensaje de información indicando que los datos se han guardado correctamente.
        """
        CED = ced.get()
        NOM = self.nom.get()
        APE = self.ape.get()
        TEL = self.tel.get()
        DIR = self.dir.get()
        DEP = self.dep.get()
        SAL = self.sal.get()
        NAC = self.nac.get()
        PUE = self.puesto.get()
        cursor.execute(
            'INSERT INTO personas (CED, NOM, APE, TEL, NAC, SAL, DIR, DEP, PUE, ORG_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (CED, NOM, APE, TEL, NAC, SAL, DIR, DEP, PUE, self.org_id))
        conexion.commit()
        print("Contenido cedula:", CED)
        print("Contenido nombre:", NOM)
        print("Contenido apellido:", APE)
        print("Contenido telefono:", TEL)
        print("Contenido direccion:", DIR)
        print("Contenido departamento:", DEP)
        print("Contenido salario:", SAL)
        print("Contenido nacionalidad:", NAC)
        print("Contenido puesto:", PUE)
        self.ced.set("")
        self.nom.set("")
        self.ape.set("")
        self.tel.set("")
        self.dir.set("")
        self.dep.set("")
        self.sal.set("")
        self.nacionality_comboBox.set("")
        self.puesto_comboBox.set("")
        messagebox.showinfo("Información", "Se han guardado correctamente los datos ingresados.")

    def regresar_entry(self):
        """
        Regresa a la ventana anterior y destruye la ventana actual.
        Guarda la referencia a la cédula ingresada.
        Destruye la ventana actual.
        Llama a la función "vincular" para volver a la ventana anterior pasando la referencia de el organigrama.
        """
        self.destroy()
        vincular(self.org_id)

    # ==================================================================================================================
    # ===================================INTERFAZ DE MODIFICAR A UNA PERSONA============================================
    # ==================================================================================================================

    def crear_interfaz_modificar(self):
        """
        Crea la interfaz gráfica para modificar la información de un empleado.
        Configura la geometría y el título de la ventana principal.
        Crea y configura el frame principal.
        Crea y configura las variables de control para los campos de entrada.
        Crea y configura los elementos de la interfaz, como etiquetas, campos de entrada y botones.
        Obtiene la lista de dependencias existentes desde la base de datos.
        Configura los combos de selección con los valores correspondientes.
        Asocia las funciones de callback a los botones.
        Ejecuta el bucle principal de la ventana.
        """
        self.geometry("600x450")
        self.title("Modificar")  # Definimos el titulo del cuadro pirncipal

        self.frame = tk.Frame(self, highlightbackground="white", highlightthickness=3)

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

        self.user_info_frame = tk.LabelFrame(self.frame, text="Informacion del empleado", font=self.tamanho_de_letra,bd=0, relief="groove")
        self.user_info_frame.grid(row=0, column=0, padx=20, pady=20)
        self.user_info_frame.config(bg=colorFondo2)


        self.ced_buscar.set("Cedula del empleado")
        self.buscar_entry = tk.Entry(self.user_info_frame, textvariable=self.ced_buscar)
        self.buscar_entry.grid(row=0, column=0, padx=15, pady=10, columnspan=4)
        self.buscar_entry.config(width=20)

        self.buscar_buttom = tk.Button(self.user_info_frame, text="BUSCAR", bg="white", fg="black", font=("Arial", 9, "bold") ,
                                       command=lambda : self.buscar_persona(self.ced_buscar))
        self.buscar_buttom.grid(row=0, column=0, sticky="nsew", pady=10)

        self.cedula_label = tk.Label(self.user_info_frame, text="Cédula", bg=colorFondo2)
        self.cedula_label.grid(row=1, column=0, padx=1)
        self.name_label = tk.Label(self.user_info_frame, text="Nombres",bg=colorFondo2)
        self.name_label.grid(row=1, column=1,padx=1)

        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.cedula_entry.grid(row=2, column=0,padx=1)

        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)
        self.nombre_entry.grid(row=2, column=1,padx=1)

        self.apellido_label = tk.Label(self.user_info_frame, text="Apellidos",bg=colorFondo2)
        self.apellido_entry = tk.Entry(self.user_info_frame, textvariable=self.ape)
        self.apellido_label.grid(row=1, column=2,padx=1)
        self.apellido_entry.grid(row=2, column=2,padx=1)

        self.phone_label = tk.Label(self.user_info_frame, text="Telefono",bg=colorFondo2)
        self.phone_label.grid(row=3, column=0,padx=1)
        self.phone_entry = tk.Entry(self.user_info_frame, textvariable=self.tel)
        self.phone_entry.grid(row=4, column=0,padx=1)

        self.nacionality_label = tk.Label(self.user_info_frame, text="Nacionalidad",bg=colorFondo2)
        self.nacionality_label.grid(row=3, column=1,padx=1)
        self.nacionality_comboBox = ttk.Combobox(self.user_info_frame,
                                                 values=["Paraguay", "Brasil", "Perú", "Argentina"])
        self.nacionality_comboBox.grid(row=4, column=1,padx=1)

        self.sueldo_label = tk.Label(self.user_info_frame, text="Salario",bg=colorFondo2)
        self.sueldo_label.grid(row=3, column=2,padx=1)
        self.sueldo_entry = tk.Entry(self.user_info_frame, textvariable=self.sal)
        self.sueldo_entry.grid(row=4, column=2,padx=1)

        self.direccion_label = tk.Label(self.user_info_frame, text="Dirección de vivienda",bg=colorFondo2)
        self.direccion_entry = tk.Entry(self.user_info_frame, textvariable=self.dir)
        self.direccion_label.grid(row=5, column=0,padx=1)
        self.direccion_entry.grid(row=6, column=0,padx=1)

        # Obtener lista de dependencias existentes
        cursor.execute('SELECT nombre FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.departamento_label = tk.Label(self.user_info_frame, text="Departamento",bg=colorFondo2)
        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.departamento_label.grid(row=5, column=1,padx=1)
        self.departamento_entry.grid(row=6, column=1,padx=1)


        self.puesto_label = tk.Label(self.user_info_frame, text="Puesto",bg=colorFondo2)
        self.puesto_label.grid(row=5, column=2,padx=1)
        self.puesto_comboBox = ttk.Combobox(self.user_info_frame,
                                            values=["Empleado", "Jefe de Departamento", "Director Ejecutivo"],
                                            textvariable=self.puesto)
        self.puesto_comboBox.grid(row=6, column=2,padx=1)

        # Botom de agregar
        self.etiqueta_agregar_buttom = tk.Button(self.frame, text="CAMBIAR",bg="white", fg="black", font=("Arial", 9, "bold") ,
                                                 command=lambda: self.cambiar_entry(self.ced))
        self.etiqueta_agregar_buttom.grid(row=7, column=0, sticky="news", padx=20, pady=1)

        self.etiqueta_regresar_buttom = tk.Button(self.frame, text="REGRESAR",bg="white", fg="black", font=("Arial", 9, "bold") ,
                                                  command=lambda: self.regresar_entry_modificar(self.ced))
        self.etiqueta_regresar_buttom.grid(row=8, column=0, sticky="news", padx=20, pady=5)

        self.mainloop()  # esta linea sirve para que la ventana principal se siga viendo hasta que cerremos

    def cambiar_entry(self, ced):
        """
        Actualiza los valores de una entrada de datos en la base de datos.
        Obtiene los valores de los campos de entrada de la interfaz.
        Realiza una consulta SQL para actualizar los datos en la base de datos.
        Muestra por consola el contenido de cada campo.
        Limpia los campos de entrada.
        Muestra una ventana de mensaje indicando que los cambios se realizaron correctamente.
        """
        CED = ced.get()
        NOM = self.nom.get()
        APE = self.ape.get()
        TEL = self.tel.get()
        DIR = self.dir.get()
        DEP = self.dep.get()
        SAL = self.sal.get()
        NAC = self.nac.get()
        PUE = self.puesto.get()

        cursor.execute(
            'UPDATE personas SET CED = ?, NOM = ?, APE = ?, TEL = ?, NAC = ?, SAL = ?, DIR = ?, DEP = ?, PUE = ?',
            (CED, NOM, APE, TEL, NAC, SAL, DIR, DEP, PUE))
        #'UPDATE dependencias SET NOMBRE = ? WHERE ID = ?', (nuevo_valor, self.dependencia_id))
        conexion.commit()

        print("Contenido cedula:", CED)
        print("Contenido nombre:", NOM)
        print("Contenido apellido:", APE)
        print("Contenido telefono:", TEL)
        print("Contenido direccion:", DIR)
        print("Contenido departamento:", DEP)
        print("Contenido salario:", SAL)
        print("Contenido nacionalidad", NAC)
        print("Contenido puesto", PUE)
        self.ced.set("")
        self.nom.set("")
        self.ape.set("")
        self.tel.set("")
        self.dir.set("")
        self.dep.set("")
        self.sal.set("")
        self.nacionality_comboBox.set("")
        self.puesto_comboBox.set("")
        self.mostrar_ventana_cambiado_correctamente()

    def mostrar_ventana_cambiado_correctamente(self):
        """
        Muestra una ventana en blanco y limpia los campos de entrada.
        Limpia los campos de entrada de la interfaz.
        Muestra una ventana en blanco.
        """
        self.ced.set("")
        self.nom.set("")
        self.ape.set("")
        self.tel.set("")
        self.dir.set("")
        self.dep.set("")
        self.sal.set("")
        self.nacionality_comboBox.set("")
        self.puesto_comboBox.set("")

        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)
        self.apellido_entry = tk.Entry(self.user_info_frame, textvariable=self.ape)
        self.phone_entry = tk.Entry(self.user_info_frame, textvariable=self.tel)
        self.direccion_entry = tk.Entry(self.user_info_frame, textvariable=self.dir)
        cursor.execute('SELECT nombre FROM dependencias')
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.departamento_label = tk.Label(self.user_info_frame, text="Departamento")
        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.sueldo_entry = tk.Entry(self.user_info_frame, textvariable=self.sal)
        self.nacionality_comboBox = ttk.Combobox(self.user_info_frame,
                                                 values=["Paraguay", "Brasil", "Perú", "Argentina"],
                                                 textvariable=self.nac)
        self.puesto_comboBox = ttk.Combobox(self.user_info_frame,
                                            values=["Empleado", "Jefe de Departamento", "Director Ejecutivo"],
                                            textvariable=self.puesto)
        self.puesto_comboBox.grid(row=6, column=2)

        messagebox.showinfo("CORRECTO", "Se modificaron los atributos correctamente.")

    def buscar_persona(self, ced):
        """
        Busca a una persona en la base de datos utilizando su número de cédula.
        Obtiene el número de cédula ingresado por el usuario.
        Realiza una consulta en la base de datos para obtener los datos de la persona correspondiente a la cédula.
        Si se encuentra un resultado, muestra los datos de la persona en los campos correspondientes.
        Si no se encuentra un resultado, muestra una ventana de error.
        """
        aux = ced.get()
        CED = self.ced_buscar.get()
        cursor.execute('SELECT CED, NOM, APE, TEL, DIR, DEP, SAL, NAC, PUE FROM personas WHERE CED = ?', (CED,))
        resultado = cursor.fetchone()
        if resultado:
            self.ced.set(resultado[0])
            self.nom.set(resultado[1])
            self.ape.set(resultado[2])
            self.tel.set(resultado[3])
            self.dir.set(resultado[4])
            self.dep.set(resultado[5])
            self.sal.set(resultado[6])
            self.nac.set(resultado[7])
            self.puesto.set(resultado[8])

            self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
            self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)
            self.apellido_entry = tk.Entry(self.user_info_frame, textvariable=self.ape)
            self.phone_entry = tk.Entry(self.user_info_frame, textvariable=self.tel)
            self.direccion_entry = tk.Entry(self.user_info_frame, textvariable=self.dir)
            cursor.execute('SELECT nombre FROM dependencias')
            lista_dependencias = [row[0] for row in cursor.fetchall()]

            self.departamento_label = tk.Label(self.user_info_frame, text="Departamento")
            self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias,
                                                   textvariable=self.dep)
            self.sueldo_entry = tk.Entry(self.user_info_frame, textvariable=self.sal)
            self.nacionality_comboBox = ttk.Combobox(self.user_info_frame, values=["Paraguay", "Brasil", "Perú", "Argentina"], textvariable=self.nac)
            self.puesto_comboBox = ttk.Combobox(self.user_info_frame,
                                                values=["Empleado", "Jefe de Departamento", "Director Ejecutivo"],
                                                textvariable=self.puesto)

            self.cedula_entry.grid(row=2, column=0)
            self.nombre_entry.grid(row=2, column= 1)
            self.apellido_entry.grid(row=2, column=2)
            self.phone_entry.grid(row=4, column=0)
            self.direccion_entry.grid(row=6, column=0)
            self.departamento_entry.grid(row=6, column=1)
            self.sueldo_entry.grid(row=4, column=2)
            self.nacionality_comboBox.grid(row=4, column=1)
            self.puesto_comboBox.grid(row=6, column=2)
        else:
            self.mostrar_ventana_error()

    def mostrar_ventana_error(self):
        """
        Muestra una ventana de error y limpia los campos de entrada.
        Reinicia los valores de las variables de los campos de entrada.
        Crea y configura nuevamente los campos de entrada en blanco.
        Muestra una ventana de error indicando que no se encontró a la persona.
        """
        self.ced.set("")
        self.nom.set("")
        self.ape.set("")
        self.tel.set("")
        self.dir.set("")
        self.dep.set("")
        self.sal.set("")
        self.nacionality_comboBox.set("")
        self.puesto_comboBox.set("")

        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)
        self.apellido_entry = tk.Entry(self.user_info_frame, textvariable=self.ape)
        self.phone_entry = tk.Entry(self.user_info_frame, textvariable=self.tel)
        self.direccion_entry = tk.Entry(self.user_info_frame, textvariable=self.dir)
        # Obtener lista de dependencias existentes
        cursor.execute('SELECT nombre FROM dependencias WHERE ORG_ID = ?', (self.org_id,))
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.departamento_label = tk.Label(self.user_info_frame, text="Departamento")
        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.departamento_label.grid(row=4, column=1)
        self.departamento_entry.grid(row=5, column=1)
        self.sueldo_entry = tk.Entry(self.user_info_frame, textvariable=self.sal)
        self.nacionality_comboBox = ttk.Combobox(self.user_info_frame,
                                                 values=["Paraguay", "Brasil", "Perú", "Argentina"],
                                                 textvariable=self.nac)
        self.puesto_comboBox = ttk.Combobox(self.user_info_frame,
                                            values=["Empleado", "Jefe de Departamento", "Director Ejecutivo"],
                                            textvariable=self.puesto)

        messagebox.showerror("Error", "No se encontró a la persona.")

    def regresar_entry_modificar(self, ced):
        """
        Vuelve a la ventana anterior para modificar la información de una persona.
        Obtiene el valor de la cédula ingresada.
        Destruye la ventana actual.
        Llama a la función "vincular" para volver a la ventana anterior y modificar los datos de la persona.
        """
        aux = ced
        self.destroy()
        vincular(self.org_id)

    # ==================================================================================================================
    # ===================================INTERFAZ DE ELIMINAR A UNA PERSONA=============================================
    # ==================================================================================================================

    def crear_interfaz_eliminar(self):
        """
        Crea la interfaz gráfica para la funcionalidad de eliminar.
        Configura el tamaño y título de la ventana.
        Crea un marco para la interfaz.
        Configura el color de fondo del marco.
        Inicializa las variables de control para los campos de entrada.
        Crea un marco para la información del empleado.
        Configura el texto y formato del campo de búsqueda.
        Crea un campo de entrada y un botón para buscar.
        Crea etiquetas y campos de entrada para mostrar la información del empleado.
        Crea etiquetas y campos de entrada para el teléfono, nacionalidad, salario, dirección y departamento.
        Crea una lista desplegable para seleccionar la nacionalidad y el puesto.
        Crea botones para eliminar y regresar.
        Ejecuta el bucle principal de la ventana para mantenerla visible.
        """
        self.geometry("600x450")
        self.title("Eliminar")

        self.frame = tk.Frame(self, highlightbackground="white", highlightthickness=3)

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
        self.puesto = StringVar()
        self.ced_buscar = StringVar()
        self.tamanho_de_letra = Font(size=15)  # tamaño de letra general"

        self.user_info_frame = tk.LabelFrame(self.frame, text="Informacion del empleado",font=self.tamanho_de_letra,bd=0, relief="groove")
        self.user_info_frame.grid(row=0, column=0, padx=20, pady=20)
        self.user_info_frame.config(bg=colorFondo3)
        self.ced_buscar.set("Cedula del empleado")
        self.buscar_entry = tk.Entry(self.user_info_frame, textvariable=self.ced_buscar)
        self.buscar_entry.grid(row=0, column=0, padx=15, pady=10, columnspan=4)
        self.buscar_entry.config(width=20)

        self.buscar_buttom = tk.Button(self.user_info_frame, text="BUSCAR",bg="white", fg="black", font=("Arial", 9, "bold"),
                                       command=lambda: self.buscar_persona_eliminar(self.ced_buscar))
        self.buscar_buttom.grid(row=0, column=0, sticky="nsew", pady=10)

        self.cedula_label = tk.Label(self.user_info_frame, text="Cédula",bg=colorFondo3)
        self.cedula_label.grid(row=1, column=0,padx=1)
        self.name_label = tk.Label(self.user_info_frame, text="Nombres",bg=colorFondo3)
        self.name_label.grid(row=1, column=1,padx=1)

        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.cedula_entry.grid(row=2, column=0,padx=1)

        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)
        self.nombre_entry.grid(row=2, column=1,padx=1)

        self.apellido_label = tk.Label(self.user_info_frame, text="Apellidos",bg=colorFondo3)
        self.apellido_entry = tk.Entry(self.user_info_frame, textvariable=self.ape)
        self.apellido_label.grid(row=1, column=2,padx=1)
        self.apellido_entry.grid(row=2, column=2,padx=1)

        self.phone_label = tk.Label(self.user_info_frame, text="Telefono",bg=colorFondo3)
        self.phone_label.grid(row=3, column=0,padx=1)
        self.phone_entry = tk.Entry(self.user_info_frame, textvariable=self.tel)
        self.phone_entry.grid(row=4, column=0,padx=1)

        self.nacionality_label = tk.Label(self.user_info_frame, text="Nacionalidad",bg=colorFondo3)
        self.nacionality_label.grid(row=3, column=1,padx=1)
        self.nacionality_comboBox = ttk.Combobox(self.user_info_frame,
                                                 values=["Paraguay", "Brasil", "Perú", "Argentina"])
        self.nacionality_comboBox.grid(row=4, column=1,padx=1)

        self.sueldo_label = tk.Label(self.user_info_frame, text="Salario",bg=colorFondo3)
        self.sueldo_label.grid(row=3, column=2,padx=1)
        self.sueldo_entry = tk.Entry(self.user_info_frame, textvariable=self.sal)
        self.sueldo_entry.grid(row=4, column=2,padx=1)

        self.direccion_label = tk.Label(self.user_info_frame, text="Dirección de vivienda",bg=colorFondo3)
        self.direccion_entry = tk.Entry(self.user_info_frame, textvariable=self.dir)
        self.direccion_label.grid(row=5, column=0,padx=1)
        self.direccion_entry.grid(row=6, column=0,padx=1)

        cursor.execute('SELECT nombre FROM dependencias')
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.departamento_label = tk.Label(self.user_info_frame, text="Departamento",bg=colorFondo3)
        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.departamento_label.grid(row=5, column=1,padx=1)
        self.departamento_entry.grid(row=6, column=1,padx=1)

        self.nacionality_comboBox = ttk.Combobox(self.user_info_frame,
                                                 values=["Paraguay", "Brasil", "Perú", "Argentina"],
                                                 textvariable=self.nac)
        self.puesto_label = tk.Label(self.user_info_frame, text="Puesto",bg=colorFondo3)
        self.puesto_comboBox = ttk.Combobox(self.user_info_frame,
                                            values=["Empleado", "Jefe de Departamento", "Director Ejecutivo"],
                                            textvariable=self.puesto)
        self.puesto_label.grid(row=5, column=2,padx=1)
        self.puesto_comboBox.grid(row=6, column=2,padx=1)

        # Boton de agregar
        self.etiqueta_agregar_buttom = tk.Button(self.frame, text="ELIMINAR",bg="white", fg="black", font=("Arial", 9, "bold"),
                                                 command=lambda: self.eliminar_entry(self.ced))
        self.etiqueta_agregar_buttom.grid(row=7, column=0, sticky="news", padx=20, pady=1)

        self.etiqueta_regresar_buttom = tk.Button(self.frame, text="REGRESAR",bg="white", fg="black", font=("Arial", 9, "bold"),
                                                  command=lambda: self.regresar_entry_eliminar(self.ced))
        self.etiqueta_regresar_buttom.grid(row=8, column=0, sticky="news", padx=20, pady=5)

        self.mainloop()  # esta linea sirve para que la ventana principal se siga viendo hasta que cerremos

    def eliminar_entry(self, ced):
        """
        Elimina una entrada de la base de datos según la cédula proporcionada.
        Obtiene los valores de los campos de entrada.
        Ejecuta una consulta para eliminar la entrada con la cédula correspondiente.
        Si se elimina alguna fila, muestra una ventana de eliminación exitosa y confirma los cambios en la base de datos.
        Si no se elimina ninguna fila, muestra una ventana de error al eliminar.
        Limpia los campos de entrada.
        """
        CED = ced.get()
        NOM = self.nom.get()
        APE = self.ape.get()
        TEL = self.tel.get()
        DIR = self.dir.get()
        DEP = self.dep.get()
        SAL = self.sal.get()
        NAC = self.nac.get()
        PUE = self.puesto.get()

        cursor.execute('DELETE FROM personas WHERE CED = ?', (CED,))
        if cursor.rowcount > 0:
            self.mostrar_ventana_eliminado_correctamente()
            conexion.commit()
        else:
            self.mostrar_ventana_error_eliminar()

        print("Contenido cedula:", CED)
        print("Contenido nombre:", NOM)
        print("Contenido apellido:", APE)
        print("Contenido telefono:", TEL)
        print("Contenido direccion:", DIR)
        print("Contenido departamento:", DEP)
        print("Contenido salario:", SAL)
        print("Contenido nacionalidad", NAC)
        print("Contenido hijos", PUE)
        self.ced.set("")
        self.nom.set("")
        self.ape.set("")
        self.tel.set("")
        self.dir.set("")
        self.dep.set("")
        self.sal.set("")
        self.nacionality_comboBox.set("")
        self.puesto_comboBox.set("")

    def buscar_persona_eliminar(self, ced):
        """
        Busca una persona en la base de datos según la cédula proporcionada y muestra la información en los campos de entrada.
        Obtiene la cédula ingresada por el usuario.
        Ejecuta una consulta para buscar la persona en la base de datos.
        Si se encuentra un resultado, muestra la información de la persona en los campos de entrada correspondientes.
        Si no se encuentra un resultado, muestra una ventana de error al eliminar.
        """
        aux = ced.get()
        CED = self.ced_buscar.get()
        cursor.execute('SELECT CED, NOM, APE, TEL, DIR, DEP, SAL, NAC, PUE FROM personas WHERE CED = ?', (CED,))
        resultado = cursor.fetchone()
        if resultado:
            # Asignar los valores a los campos de entrada correspondientes
            self.ced.set(resultado[0])
            self.nom.set(resultado[1])
            self.ape.set(resultado[2])
            self.tel.set(resultado[3])
            self.dir.set(resultado[4])
            self.dep.set(resultado[5])
            self.sal.set(resultado[6])
            self.nac.set(resultado[7])
            self.puesto.set(resultado[8])

            # Crear y colocar los widgets de entrada correspondientes
            self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
            self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)
            self.apellido_entry = tk.Entry(self.user_info_frame, textvariable=self.ape)
            self.phone_entry = tk.Entry(self.user_info_frame, textvariable=self.tel)
            self.direccion_entry = tk.Entry(self.user_info_frame, textvariable=self.dir)
            cursor.execute('SELECT nombre FROM dependencias')
            lista_dependencias = [row[0] for row in cursor.fetchall()]

            self.departamento_label = tk.Label(self.user_info_frame, text="Departamento")
            self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias,
                                                   textvariable=self.dep)
            self.sueldo_entry = tk.Entry(self.user_info_frame, textvariable=self.sal)
            self.nacionality_comboBox = ttk.Combobox(self.user_info_frame,
                                                     values=["Paraguay", "Brasil", "Perú", "Argentina"],
                                                     textvariable=self.nac)
            self.puesto_comboBox = ttk.Combobox(self.user_info_frame,
                                                values=["Empleado", "Jefe de Departamento", "Director Ejecutivo"],
                                                textvariable=self.puesto)

            self.cedula_entry.grid(row=2, column=0)
            self.nombre_entry.grid(row=2, column=1)
            self.apellido_entry.grid(row=2, column=2)
            self.phone_entry.grid(row=4, column=0)
            self.direccion_entry.grid(row=6, column=0)
            self.departamento_entry.grid(row=6, column=1)
            self.sueldo_entry.grid(row=4, column=2)
            self.nacionality_comboBox.grid(row=4, column=1)
            self.puesto_comboBox.grid(row=6, column=2)
        else:
            self.mostrar_ventana_error_eliminar()

    def mostrar_ventana_error_eliminar(self):
        """
        Muestra una ventana de error al intentar eliminar a una persona.
        Restablece los valores de las variables asociadas a los campos de entrada.
        Crea nuevos objetos Entry y Combobox para los campos de entrada.
        Muestra un mensaje de error indicando que no se encontró a la persona.
        """

        self.ced.set("")
        self.nom.set("")
        self.ape.set("")
        self.tel.set("")
        self.dir.set("")
        self.dep.set("")
        self.sal.set("")
        self.nacionality_comboBox.set("")
        self.puesto_comboBox.set("")

        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)
        self.apellido_entry = tk.Entry(self.user_info_frame, textvariable=self.ape)
        self.phone_entry = tk.Entry(self.user_info_frame, textvariable=self.tel)
        self.direccion_entry = tk.Entry(self.user_info_frame, textvariable=self.dir)

        cursor.execute('SELECT nombre FROM dependencias')
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.departamento_label = tk.Label(self.user_info_frame, text="Departamento")
        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.sueldo_entry = tk.Entry(self.user_info_frame, textvariable=self.sal)
        self.nacionality_comboBox = ttk.Combobox(self.user_info_frame,
                                                 values=["Paraguay", "Brasil", "Perú", "Argentina"],
                                                 textvariable=self.nac)
        self.puesto_comboBox = ttk.Combobox(self.user_info_frame,
                                            values=["Empleado", "Jefe de Departamento", "Director Ejecutivo"],
                                            textvariable=self.puesto)

        messagebox.showerror("Error", "No se encontró a la persona.")

    def mostrar_ventana_eliminado_correctamente(self):
        """
        Muestra una ventana indicando que una persona ha sido eliminada correctamente.
        Restablece los valores de las variables asociadas a los campos de entrada.
        Crea nuevos objetos Entry y Combobox para los campos de entrada.
        Muestra un mensaje informativo indicando que la persona ha sido eliminada correctamente.
        """
        self.ced.set("")
        self.nom.set("")
        self.ape.set("")
        self.tel.set("")
        self.dir.set("")
        self.dep.set("")
        self.sal.set("")
        self.nacionality_comboBox.set("")

        self.cedula_entry = tk.Entry(self.user_info_frame, textvariable=self.ced)
        self.nombre_entry = tk.Entry(self.user_info_frame, textvariable=self.nom)
        self.apellido_entry = tk.Entry(self.user_info_frame, textvariable=self.ape)
        self.phone_entry = tk.Entry(self.user_info_frame, textvariable=self.tel)
        self.direccion_entry = tk.Entry(self.user_info_frame, textvariable=self.dir)
        cursor.execute('SELECT nombre FROM dependencias')
        lista_dependencias = [row[0] for row in cursor.fetchall()]

        self.departamento_label = tk.Label(self.user_info_frame, text="Departamento")
        self.departamento_entry = ttk.Combobox(self.user_info_frame, values=lista_dependencias, textvariable=self.dep)
        self.sueldo_entry = tk.Entry(self.user_info_frame, textvariable=self.sal)
        self.nacionality_comboBox = ttk.Combobox(self.user_info_frame,
                                                 values=["Paraguay", "Brasil", "Perú", "Argentina"],
                                                 textvariable=self.nac)
        self.puesto_comboBox = ttk.Combobox(self.user_info_frame,
                                            values=["Empleado", "Jefe de Departamento", "Director Ejecutivo"],
                                            textvariable=self.puesto)

        messagebox.showinfo("CORRECTO", "Se dio de baja a la persona correctamente")

    def regresar_entry_eliminar(self, ced):
        """
        Regresa a la ventana anterior y actualiza la interfaz.
        Guarda el valor de la cédula.
        Destruye la ventana actual.
        Llama a la función "vincular" para abrir la ventana anterior y pasar el ID de el organigrama.
        """
        aux = ced
        self.destroy()
        vincular(self.org_id)

def Abrir_Vincular(org_id):
    """
    Abre la ventana "vincular" con el ID de el organigrama proporcionado.
    Llama a la función "vincular" y pasa el ID de el organigrama como argumento.
    """
    programa = vincular(org_id)






