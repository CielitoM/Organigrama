import tkinter as tk
import sqlite3
from tkinter import messagebox

conexion = sqlite3.connect('organigrama.db')
cursor = conexion.cursor()


class VInformes(tk.Tk):
    def __init__(self, org_id):
        tk.Tk.__init__(self)

        self.title('Informes')
        self.org_id = org_id

        self.dependencias = cursor.execute(f'''SELECT ID, NOMBRE 
                                            FROM dependencias WHERE ORG_ID = {org_id}''').fetchall()
        print(list(self.dependencias))

        self.geometry('600x450')
        self.config(bg="#FF2525")

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, column=0)

        self.frame_botones_inferiores = tk.Frame(self)
        self.frame_botones_inferiores.grid(row=1, column=0)

        self.botones = tk.LabelFrame(self.frame)
        self.botones.grid(row=0, column=0)
        self.botones.config(bg="#FF2525")

        self.value_inside = tk.StringVar(self.botones)
        self.value_inside.set('Seleccione una dependencia')
        self.seleccionardep = tk.OptionMenu(self.botones, self.value_inside, *self.dependencias)
        self.seleccionardep.config(bg="white", fg="black", font=("Arial", 9, "bold"))
        self.seleccionardep.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.etiqueta_Informe1 = tk.Button(self.botones, text="Personal por dependencia", bg="white", fg="black", font=("Arial", 9, "bold"), command=self.personal_por_dependencia)
        self.etiqueta_Informe1.grid(row=1, column=0, sticky="nsew", padx=5, pady=1)

        self.etiqueta_Informe2 = tk.Button(self.botones, text="Personal por dependencia extendido", bg="white", fg="black", font=("Arial", 9, "bold"), command=self.personal_por_dependencia_ext)
        self.etiqueta_Informe2.grid(row=2, column=0, sticky="nsew", padx=5, pady=1)

        self.etiqueta_Informe3 = tk.Button(self.botones, text="Salario por dependencia", bg="white", fg="black", font=("Arial", 9, "bold"), command=self.salario_por_dependencia)
        self.etiqueta_Informe3.grid(row=3, column=0, sticky="nsew", padx=5, pady=1)

        self.regresar_Informe4 = tk.Button(self.botones, text="Salario por dependencia extendido", bg="white", fg="black", font=("Arial", 9, "bold"), command=self.salario_por_dependencia_ext)
        self.regresar_Informe4.grid(row=4, column=0, sticky="nsew", padx=5, pady=1)

        self.regresar_Informe5 = tk.Button(self.botones, text="REGRESAR", bg="white", fg="black", font=("Arial", 9, "bold"), command=self.regresar)
        self.regresar_Informe5.grid(row=5, column=0, sticky="nsew", padx=5, pady=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.botones.columnconfigure(0, weight=1)
        self.botones.rowconfigure(0, weight=1)
        self.botones.rowconfigure(1, weight=1)
        self.botones.rowconfigure(2, weight=1)

        self.update_idletasks()  # Actualizar la ventana antes de obtener el tamaño

        # Posicionar ventana después de self.update_idletasks()
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
        cursor.execute('SELECT USUARIO_ID FROM organigrama WHERE ID = ?', (self.org_id,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
            print("USUARIO ID EN BUSCAR USUARIO:", user_id)
            return user_id
        else:
            return None

    def regresar(self):
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


    def personal_por_dependencia(self):
        """
        Muestra una ventana emergente con el personal ordenado por dependencia.
        Obtiene la dependencia seleccionada por el usuario.
        Convierte la dependencia en una lista de elementos.
        Obtiene el nombre de la dependencia de la lista.
        Elimina los caracteres de comillas de la dependencia.
        Consulta la base de datos para obtener el personal de la dependencia y organigrama seleccionadas.
        Ordena el personal alfabéticamente por apellido.
        Crea una ventana emergente para mostrar la lista de personal.
        Centra la ventana emergente en la pantalla.
        """
        dep = self.value_inside.get()

        print(dep)
        dep = dep[1:-1]

        dep_li = list(dep.split(", "))
        print(dep_li)

        dep_nom = dep_li[1]
        print(dep_nom)

        # Eliminar los caracteres ' de dep_nom
        dep_nom = dep_nom.replace("'", "")

        cursor.execute("SELECT NOM, APE FROM personas WHERE DEP = ? AND ORG_ID = ?", (dep_nom, self.org_id))
        personal = cursor.fetchall()

        tuplas_ordenadas = sorted(personal, key=lambda x: x[1])
        mensaje = tk.Tk()
        mensaje.title('Personal')
        mensaje.geometry('300x250')
        mensaje.config(bg="#FF2525")

        titulo1 = tk.Label(mensaje, text="            Personal por dependencia",
                           font=("Segoe UI Black", 10), fg="#FFFFFF", bg="#FF2525")
        titulo1.place(x=20, y=5)
        lista = tk.Listbox(mensaje)
        lista.place(x= 20, y = 60)
        lista.config(height=10, width=43)

        for tupla in tuplas_ordenadas:
            cadena = ' - '.join(map(str, tupla))
            lista.insert(tk.END, cadena)

        # Obtener el tamaño de la pantalla
        screen_width = mensaje.winfo_screenwidth()
        screen_height = mensaje.winfo_screenheight()

        # Obtener el tamaño de la ventana
        window_width = mensaje.winfo_reqwidth()
        window_height = mensaje.winfo_reqheight()

        # Calcular la posición x, y para centrar la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Posicionar la ventana en el centro de la pantalla
        mensaje.geometry(f"+{x}+{y}")

        mensaje.mainloop()

    def personal_por_dependencia_ext(self):
        """
        Obtiene y muestra el personal por dependencia extendido.
        Obtiene la dependencia seleccionada por el usuario.
        Verifica si la dependencia seleccionada es la dependencia principal del organigrama.
        Si es la dependencia principal, obtiene las personas que pertenecen al ORG_ID especificado.
        Si no es la dependencia principal, obtiene las dependencias hijas indirectas o directas de la dependencia seleccionada y las personas asociadas.
        Muestra los nombres y apellidos de las personas obtenidas en una ventana gráfica.
        Centra la ventana en la pantalla.
        """
        global personas
        dep = self.value_inside.get()
        dep = dep[1:-1]
        dep_li = list(dep.split(", "))
        dep_nom = dep_li[1]

        # Eliminar los caracteres ' de dep_nom
        dep_nom = dep_nom.replace("'", "")

        # Obtener la dependencia principal del organigrama con DEPENDENCIA_PADRE_ID = 0 y ORG_ID = org_id
        dependencia_principal = cursor.execute(
            f"SELECT ID, NOMBRE FROM dependencias WHERE DEPENDENCIA_PADRE_ID = 0 AND ORG_ID = {self.org_id}"
        ).fetchone()

        print("DEPENDENCIA PRINCIPAL:", dependencia_principal[1])
        print("DEPENDENCIA SELECCIONADA POR EL USUARIO:", dep_nom)

        if dependencia_principal[1] == dep_nom:
            print("Se ha ingresado en dependencia principal porque es igual que la que ha seleccionado el usuario")
            # Procedimiento cuando la opción seleccionada es la dependencia cabeza del organigrama
            # Obtener las personas que pertenecen al ORG_ID especificado
            personas = cursor.execute(
                f"SELECT NOM, APE FROM personas WHERE ORG_ID = {self.org_id}").fetchall()

            # Imprimir los nombres y apellidos de las personas
            for persona in personas:
                nombre = persona[0]
                apellido = persona[1]
                print(nombre, apellido)


        else:
            # Procedimiento cuando la opción seleccionada no es la dependencia principal del organigrama
            # Obtener una lista de todas las dependencias hijas indirectas o directas de la dependencia seleccionada y que pertenecen al ORG_ID especificado
            dependencias_hijas = self.obtener_dependencias_hijas(dep_nom, self.org_id)
            dependencias_hijas.append(dep_nom)  # Agregar la dependencia seleccionada como raíz
            personas = self.obtener_personas_por_dependencias(dependencias_hijas, self.org_id)

            # Imprimir los nombres y apellidos de las personas
            for persona in personas:
                nombre = persona[0]
                apellido = persona[1]
                print(nombre, apellido)

        mensaje = tk.Tk()
        mensaje.title("Personal")
        mensaje.geometry("300x250")
        mensaje.config(bg="#FF2525")
        mensaje.resizable(False, False)

        titulo1 = tk.Label(mensaje, text="   Personal por dependencia extendido", font=("Segoe UI Black", 10),
                           fg="#FFFFFF", bg="#FF2525")
        titulo1.place(x=20, y=5)
        lista = tk.Listbox(mensaje)
        lista.place(x=20, y=60)
        lista.config(height=10, width=43)

        for persona in personas:
            nombre = persona[0]
            apellido = persona[1]
            cadena = f"{nombre} {apellido}"
            lista.insert(tk.END, cadena)

        # Obtener el tamaño de la pantalla
        screen_width = mensaje.winfo_screenwidth()
        screen_height = mensaje.winfo_screenheight()

        # Obtener el tamaño de la ventana
        window_width = mensaje.winfo_reqwidth()
        window_height = mensaje.winfo_reqheight()

        # Calcular la posición x, y para centrar la ventana
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Posicionar la ventana en el centro de la pantalla
        mensaje.geometry(f"+{x}+{y}")
        mensaje.mainloop()

    def obtener_personas_por_dependencias(self, dependencias, org_id):
        """
        Obtiene las personas que pertenecen a las dependencias especificadas y a una organigrama determinada.

        Recibe una lista de dependencias y el ID de el organigrama.
        Construye una cadena con las dependencias separadas por comas para usar en la consulta SQL.
        Realiza una consulta SQL para obtener las personas que pertenecen a las dependencias y organigrama especificadas.
        Recorre los resultados de la consulta y almacena los nombres y apellidos en una lista de tuplas.
        Devuelve la lista de personas encontradas.
        """
        personas = []

        # Construir una cadena con las dependencias separadas por comas para usar en la consulta SQL
        dependencias_str = ", ".join(f"'{dep}'" for dep in dependencias)

        # Consulta SQL para obtener las personas que pertenecen a las dependencias hijas
        query = f"SELECT NOM, APE FROM personas WHERE DEP IN ({dependencias_str}) AND ORG_ID = {org_id}"
        cursor.execute(query)

        # Recorrer los resultados y almacenar los nombres y apellidos en una tupla
        for row in cursor.fetchall():
            personas.append((row[0], row[1]))

        return personas

    def obtener_dependencias_hijas(self, dep_nom, org_id):
        """
        Obtiene las dependencias hijas de una dependencia dada.

        :parameter
            - dep_nom: Nombre de la dependencia padre.
            - org_id: ID de el organigrama.

        :return
            - Una lista con los nombres de las dependencias hijas.
        """
        # Buscar el ID de la dependencia seleccionada
        cursor.execute("SELECT ID FROM dependencias WHERE NOMBRE = ? AND ORG_ID = ?", (dep_nom, org_id))
        dep_id = cursor.fetchone()[0]

        # Llamar a la función recursiva para obtener las dependencias hijas
        dependencias_hijas = self.obtener_dependencias_recursivas(dep_id, org_id)

        # Retornar una lista con los nombres de las dependencias hijas
        return dependencias_hijas

    def obtener_dependencias_recursivas(self, dep_id, org_id):
        """
        Obtiene de forma recursiva las dependencias hijas de una dependencia dada.

        :parameter
            - dep_id: ID de la dependencia padre.
            - org_id: ID de el organigrama.

        :return
            - Una lista con los nombres de las dependencias hijas.
        """
        # Buscar las dependencias directas de la dependencia actual
        cursor.execute("SELECT NOMBRE FROM dependencias WHERE DEPENDENCIA_PADRE_ID = ? AND ORG_ID = ?",
                       (dep_id, org_id))
        dependencias_directas = cursor.fetchall()

        # Lista para almacenar todas las dependencias hijas, incluyendo las descendientes indirectas
        dependencias_hijas = []

        # Recorrer las dependencias directas y obtener sus dependencias hijas recursivamente
        for dep_directa in dependencias_directas:
            dependencias_hijas.append(dep_directa[0])
            dependencias_hijas.extend(self.obtener_dependencias_recursivas(dep_directa[0], org_id))

        return dependencias_hijas

    def obtener_dependencias_completas(self, dep_id):
        """
        Obtiene todas las dependencias descendientes de una dependencia dada.
        :parameter
            - dep_id: ID de la dependencia.

        :return
            - Una lista con los IDs de todas las dependencias descendientes.
        """
        dependencias_completas = [dep_id]
        dependencias_hijas = cursor.execute(
            "SELECT ID FROM dependencias WHERE DEPENDENCIA_PADRE_ID = ?", (dep_id,)
        ).fetchall()
        for dep_hija in dependencias_hijas:
            dependencias_completas.extend(self.obtener_dependencias_completas(dep_hija[0]))
        return dependencias_completas

    def salario_por_dependencia(self):
        """
        Calcula el salario total y el total de empleados por dependencia.
        Obtiene la dependencia seleccionada por el usuario.
        Realiza consultas a la base de datos para obtener el salario total y el total de empleados de la dependencia.
        Muestra una ventana de diálogo con la información obtenida.
        """
        dep = self.value_inside.get()
        dep = dep[1:-1]
        dep_li = list(dep.split(", "))
        dep_nom = dep_li[1]
        # Eliminar los caracteres ' de dep_nom
        dep_nom = dep_nom.replace("'", "")
        cursor.execute("SELECT SUM(SAL) FROM personas WHERE DEP = ? AND ORG_ID = ?", (dep_nom, self.org_id))
        salario_total = cursor.fetchall()
        cursor.execute("SELECT count(NOM) FROM personas WHERE DEP = ? AND ORG_ID = ?", (dep_nom, self.org_id))
        total_empleados = cursor.fetchall()
        print(salario_total[0][0])

        messagebox.showinfo('Salario Total', f'Salario de {dep_nom}: {salario_total[0][0]} G.\n'
                                             f'Total Empleados: {total_empleados[0][0]}')

    def salario_por_dependencia_ext(self):
        """
        Calcula el salario total y el número total de empleados para una dependencia seleccionada.

        Obtiene la dependencia seleccionada por el usuario.
        Extrae el nombre de la dependencia de la cadena.
        Verifica si la dependencia seleccionada es la dependencia principal del organigrama.
        Si es la dependencia principal, calcula el salario total y el número total de empleados para todo el organigrama.
        Si no es la dependencia principal, obtiene todas las dependencias hijas indirectas o directas de la dependencia seleccionada.
        Obtiene las personas asociadas a las dependencias obtenidas.
        Calcula el salario total y el número total de empleados para la dependencia seleccionada y sus dependencias hijas.
        Muestra un cuadro de diálogo con el salario total y el número total de empleados.
        """
        dep = self.value_inside.get()
        dep = dep[1:-1]
        dep_li = list(dep.split(", "))
        dep_nom = dep_li[1]

        # Eliminar los caracteres ' de dep_nom
        dep_nom = dep_nom.replace("'", "")

        # Obtener la dependencia principal del organigrama con DEPENDENCIA_PADRE_ID = 0 y ORG_ID = org_id
        dependencia_principal = cursor.execute(
            f"SELECT ID, NOMBRE FROM dependencias WHERE DEPENDENCIA_PADRE_ID = 0 AND ORG_ID = {self.org_id}"
        ).fetchone()

        print("DEPENDENCIA PRINCIPAL:", dependencia_principal[1])
        print("DEPENDENCIA SELECCIONADA POR EL USUARIO:", dep_nom)

        if dependencia_principal[1] == dep_nom:
            print("Se ha ingresado en dependencia principal porque es igual que la que ha seleccionado el usuario")
            # Procedimiento cuando la opción seleccionada es la dependencia cabeza del organigrama
            # Obtener la suma de salarios de personas que pertenecen al ORG_ID especificado
            cursor.execute(f"SELECT SUM(SAL) FROM personas WHERE ORG_ID = {self.org_id}")
            salariototal = cursor.fetchone()[0]
            # Obtener la cantidad de personas en todo el organigrama
            cursor.execute(f"SELECT COUNT(*) FROM personas WHERE ORG_ID = {self.org_id}")
            total_empleados = cursor.fetchone()[0]

            messagebox.showinfo('Salario Total', f'Salario de {dep_nom} hacia abajo: {salariototal} G.\n'
                                                 f'Total Empleados: {total_empleados}')

        else:
            # Procedimiento cuando la opción seleccionada no es la dependencia principal del organigrama
            # Obtener una lista de todas las dependencias hijas indirectas o directas de la dependencia seleccionada y que pertenecen al ORG_ID especificado
            dependencias_hijas = self.obtener_dependencias_hijas(dep_nom, self.org_id)
            dependencias_hijas.append(dep_nom)  # Agregar la dependencia seleccionada como raíz
            personas = self.obtener_personas_por_dependencias(dependencias_hijas, self.org_id)

            # Imprimir los nombres y apellidos de las personas
            for persona in personas:
                nombre = persona[0]
                apellido = persona[1]
                print(nombre, apellido)

            salario_total = 0
            for persona in personas:
                cursor.execute("SELECT SAL FROM personas WHERE NOM = ? AND APE = ? AND ORG_ID = ?",
                               (persona[0], persona[1], self.org_id))
                salario_persona = cursor.fetchone()[0]
                salario_total += int(salario_persona)

            total_empleados = len(personas)

            messagebox.showinfo('Salario Total', f'Salario de {dep_nom}: {salario_total} G.\n'
                                                 f'Total Empleados: {total_empleados}')
