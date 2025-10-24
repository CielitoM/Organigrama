import tkinter as tk
import sqlite3
from tkinter import messagebox
from HOME import VentanaPrincipal
from PIL import ImageTk, Image
import sys  # Libreria para cerrar bien el programa (Mirar metodo cerrar_programa)


class VentanaInicioSesion(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Crear la conexión a la base de datos
        self.conexion = sqlite3.connect('organigrama.db')
        self.cursor = self.conexion.cursor()

        # Configuración de la ventana de inicio de sesión
        self.geometry("600x450")
        self.title("Inicio de Sesión")
        self.resizable(False, False)

        # Variables para el color del frame izquierdo y los botones
        self.color_frame = '#FF2525'
        self.color_botones = '#FF2525'

        # Llamada a los métodos
        self.Frames()
        self.Modulos()
        self.pos_login()

    def pos_login(self):
        """
        Posiciona la ventana de inicio de sesión en el centro de la pantalla.
        """
        self.update_idletasks()
        ancho = self.winfo_width()
        largo = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (largo // 2)
        self.geometry('{}x{}+{}+{}'.format(ancho, largo, x, y))

    def Frames(self):
        """
        Crea y configura los frames de la ventana.
        Genera dos frames: frame_izquierda y frame_modulos.
        Agrega un logo en el frame_izquierda y establece su fondo.
        Configura el tamaño de frame_izquierda.
        Ubica los frames utilizando el administrador de geometría pack.
        """
        # Creación de los frames
        self.frame_izquierda = tk.Frame(self, bg=self.color_frame, bd=1, relief="ridge")
        self.frame_modulos = tk.Frame(self, bd=4, relief="ridge", bg="white")

        # Agregar el logo en el frame izquierda
        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((200, 200))
        logo_image = ImageTk.PhotoImage(logo_image)

        # Establecer el fondo del logo_label como el fondo del frame_izquierda
        logo_label = tk.Label(self.frame_izquierda, image=logo_image, bg=self.color_frame)
        logo_label.image = logo_image  # Conservar una referencia para evitar que la imagen sea recolectada por el
        # recolector de basura
        logo_label.place(x=70, y=113)

        # Tamaño de los frames
        self.frame_izquierda.config(width=120)

        # Ubicación de los frames utilizando el administrador de geometría pack
        self.frame_izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frame_modulos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def Modulos(self):
        """
        Crea los elementos de la interfaz de usuario para los módulos.
        Crea campos de entrada para el nombre de usuario y la contraseña.
        Crea botones para iniciar sesión, registrarse y cerrar el programa.
        Configura las propiedades de los elementos creados, como texto, fuentes, colores y dimensiones.
        Asigna los comandos correspondientes a los botones.
        Ubica los elementos en la interfaz utilizando las coordenadas (x, y).
        """
        # Creación de los campos de entrada (entry widgets)
        nombre_label = tk.Label(self.frame_modulos, text="Nombre de usuario", font=("Arial", 12), bg="white")
        self.nombre_entry = tk.Entry(self.frame_modulos, width=27, highlightbackground="#E5D8D8",
                                     highlightcolor="#E5D8D8", highlightthickness=1)
        nombre_label.place(x=40, y=100)
        self.nombre_entry.place(x=40, y=130)

        contra_label = tk.Label(self.frame_modulos, text="Contraseña", font=("Arial", 12), bg="white")
        self.contra_entry = tk.Entry(self.frame_modulos, width=27, show="*", highlightbackground="#E5D8D8",
                                     highlightcolor="#E5D8D8", highlightthickness=1)
        contra_label.place(x=40, y=160)
        self.contra_entry.place(x=40, y=190)

        btn_iniciar_sesion = tk.Button(self.frame_modulos, text="Iniciar Sesión", bg=self.color_botones, fg="white",
                                       font=("Arial", 10, "bold"), width=20, height=1, command=self.iniciar_sesion)
        btn_iniciar_sesion.place(x=40, y=240)

        btn_registrarse = tk.Button(self.frame_modulos, text="Registrarse", bg=self.color_botones, fg="white",
                                    font=("Arial", 10, "bold"), width=20, height=1, command=self.registrarse)
        btn_registrarse.place(x=40, y=290)

        btn_registrarse = tk.Button(self.frame_modulos, text="Cerrar Programa", bg=self.color_botones, fg="white",
                                    font=("Arial", 10, "bold"), width=20, height=1, command=self.cerrar_programa)
        btn_registrarse.place(x=40, y=400)

    def cerrar_ventana(self):
        """
        Cierra la ventana de inicio de sesión.
        Destruye la ventana actual y finaliza su ejecución.
        """
        self.destroy()

    def iniciar_sesion(self):
        """
        Inicia el proceso de inicio de sesión.
        Obtiene el nombre de usuario y la contraseña ingresados por el usuario.
        Verifica que se hayan ingresado ambos campos.
        Consulta la base de datos para verificar las credenciales ingresadas.
        Si las credenciales son correctas, se inicia sesión exitosamente.
        Se obtiene el ID de usuario correspondiente.
        Se cierra la ventana de inicio de sesión y se abre la ventana principal.
        Si las credenciales son incorrectas, se muestra un mensaje de error.
        """
        nombre = self.nombre_entry.get()
        contra = self.contra_entry.get()

        if nombre == "" or contra == "":
            messagebox.showerror("Error", "Debe ingresar nombre de usuario y contraseña.")
            return

        if len(nombre) < 1 or len(nombre) > 20:
            messagebox.showerror("Error", "El nombre de usuario debe tener entre 1 y 20 caracteres.")
            return

        if len(contra) < 1 or len(contra) > 20:
            messagebox.showerror("Error", "La contraseña debe tener entre 1 y 20 caracteres.")
            return

        # Consultar la base de datos para verificar las credenciales
        self.cursor.execute('SELECT * FROM usuario WHERE NOMBRE=? AND CONTRA=?', (nombre, contra))
        resultado = self.cursor.fetchone()

        if resultado:
            # Iniciar sesión exitosamente
            # messagebox.showinfo("Inicio de sesión", "Sesión iniciada correctamente.")
            # Obtener el ID de usuario
            global user_id
            user_id = resultado[0]
            print("ID USUARIO: ", user_id)
            # Abrir la ventana principal después del inicio de sesión exitoso
            self.cerrar_ventana()
            ventana_principal = VentanaPrincipal(user_id)
            # Ejecutar el bucle principal de la ventana principal solo si se ha iniciado sesión correctamente
            ventana_principal.mainloop()
            self.cerrar_ventana()
        else:
            # Credenciales incorrectas
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")

    def registrarse(self):
        """
        Realiza el proceso de registro de un nuevo usuario.
        Obtiene el nombre de usuario y la contraseña ingresados por el usuario.
        Verifica que se hayan ingresado ambos campos.
        Verifica la longitud de las cadenas ingresadas.
        Consulta la base de datos para verificar si el nombre de usuario ya existe.
        Si el nombre de usuario ya existe, muestra un mensaje de error.
        Si el nombre de usuario no existe, inserta el nuevo usuario en la base de datos.
        Muestra un mensaje de registro exitoso.
        Limpia los campos de entrada.
        """
        nombre = self.nombre_entry.get()
        contra = self.contra_entry.get()

        if nombre == "" or contra == "":
            messagebox.showerror("Error", "Por favor, ingrese nombre de usuario y contraseña.")
            return

        if len(nombre) < 1 or len(nombre) > 20:
            messagebox.showerror("Error", "El nombre de usuario debe tener entre 1 y 20 caracteres.")
            return

        if len(contra) < 1 or len(contra) > 20:
            messagebox.showerror("Error", "La contraseña debe tener entre 1 y 20 caracteres.")
            return

        # Verificar si el nombre de usuario ya existe en la base de datos
        self.cursor.execute('SELECT * FROM usuario WHERE NOMBRE=?', (nombre,))
        usuario = self.cursor.fetchone()

        if usuario is not None:
            messagebox.showerror("Error", "El nombre de usuario ya existe.")
            return

        # Insertar el nuevo usuario en la base de datos
        self.cursor.execute('INSERT INTO usuario (NOMBRE, CONTRA) VALUES (?, ?)', (nombre, contra))
        self.conexion.commit()

        messagebox.showinfo("Registro exitoso", "El usuario ha sido registrado correctamente.")

        # Limpiar los campos de entrada
        self.nombre_entry.delete(0, tk.END)
        self.contra_entry.delete(0, tk.END)

    def cerrar_programa(self):
        """
        Cierra el programa por completo.
        Da foco a la ventana principal antes de cerrarla.
        Destruye la ventana principal.
        Sale del programa completamente.
        """
        self.focus_force()  # Dar foco a la ventana principal antes de cerrarla
        self.destroy()
        sys.exit(0)  # Salir del programa completamente


# Crear la ventana de inicio de sesión
ventana_inicio_sesion = VentanaInicioSesion()
ventana_inicio_sesion.mainloop()
