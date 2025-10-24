import sqlite3
import os
import graphviz

# Conexión a la base de datos "organigrama.db"
conn = sqlite3.connect("organigrama.db")
cursor = conn.cursor()

# Crear la base de datos "arbol" y las tablas "nodos" y "aristas"
cursor.execute('''CREATE TABLE IF NOT EXISTS nodos (
                    id INTEGER PRIMARY KEY,
                    nombre TEXT,
                    tipo TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS aristas (
                    id INTEGER PRIMARY KEY,
                    nodo_padre_id INTEGER,
                    nodo_hijo_id INTEGER,
                    FOREIGN KEY (nodo_padre_id) REFERENCES nodos (id),
                    FOREIGN KEY (nodo_hijo_id) REFERENCES nodos (id)
                )''')

def buscar_usuario_id(org_id):
    """
    Busca el ID de usuario asociado a un ID de organigrama en la base de datos.
    Recibe el ID del organigrama como parámetro.
    Consulta la base de datos para obtener el ID de usuario asociado al ID de organigrama.
    Si se encuentra el resultado, devuelve el ID de usuario.
    Si no se encuentra el resultado, devuelve None.
    """
    cursor.execute('SELECT USUARIO_ID FROM organigrama WHERE ID = ?', (org_id,))
    result = cursor.fetchone()
    if result:
        user_id = result[0]
        print("USUARIO ID EN BUSCAR USUARIO:", user_id)
        return user_id
    else:
        return None

def Regresar_A_Inicio(org_id):
    """
    Regresa a la ventana de inicio.
    Recibe el ID de el organigrama como parámetro.
    Busca el ID del usuario correspondiente a el organigrama.
    Crea una nueva instancia de la ventana principal y la muestra.
    """
    user_id = buscar_usuario_id(org_id)
    print("USUARIO ID EN REGRESAR A INICIO:", user_id)
    from HOME import VentanaPrincipal
    VentanaPrincipal(user_id)  # Crear una nueva instancia de la ventana principal

def crear_arbol(dep, org_id):
    """
    Crea y muestra un organigrama a partir de las dependencias y jefes de departamento en una base de datos.

    :parameter:
        dep: El nombre de la dependencia raíz.
        org_id: El ID de el organigrama.

    :return:
        No retorna nada
        (Una vez que termina regresa a HOME)
    """
    # Obtener el jefe de departamento
    cursor.execute(
        "SELECT NOM || ' ' || APE FROM personas WHERE ORG_ID = ? AND DEP = ? AND PUE = 'Jefe de Departamento'",
        (org_id, dep))
    jefe_departamento = cursor.fetchone()
    if jefe_departamento:
        jefe_departamento = jefe_departamento[0]
    else:
        jefe_departamento = "(Sin Jefe Asignado)"

    print("JEFE DE DEPARTAMENTO ES:", jefe_departamento)

    # Obtener el ID de la dependencia raíz
    cursor.execute("SELECT ID FROM dependencias WHERE NOMBRE = ? AND ORG_ID = ?", (dep, org_id))
    dependencia_id = cursor.fetchone()[0]

    if jefe_departamento:
        if jefe_departamento == "(Sin Jefe Asignado)":
            nombre_departamento = dep
        else:
            nombre_departamento = f"{dep}. \n(Jefe {jefe_departamento})"
    else:
        nombre_departamento = dep

    # Insertar el nodo raíz en la tabla "nodos"
    cursor.execute("INSERT INTO nodos (id, nombre, tipo) VALUES (?, ?, ?)", (dependencia_id, nombre_departamento, "Raíz"))

    # Función para insertar las subdependencias en la tabla "nodos" y "aristas"
    def insertar_subdependencias(dep_padre_id, nodo_padre_id):
        """
        Inserta las subdependencias en la base de datos y establece las relaciones entre los nodos.

        Recibe el ID de la dependencia padre y el ID del nodo padre.
        Obtiene las subdependencias de la base de datos.
        Busca el jefe de departamento de cada subdependencia.
        Inserta los nodos de las subdependencias en la tabla "nodos".
        Establece las relaciones entre el nodo padre y los nodos hijos en la tabla "aristas".
        Llama recursivamente a la función para las subdependencias.
        """
        cursor.execute("SELECT ID, NOMBRE FROM dependencias WHERE DEPENDENCIA_PADRE_ID = ? AND ORG_ID = ?",
                       (dep_padre_id, org_id))
        subdependencias = cursor.fetchall()
        for subdep in subdependencias:
            print("ORG ID AL BUSCAR EL JEFE DE SUBDEPENDENCIAS ES:", org_id)
            cursor.execute(
                "SELECT NOM || ' ' || APE FROM personas WHERE ORG_ID = ? AND DEP = ? AND PUE = 'Jefe de Departamento'",
                (org_id, subdep[1]))
            jefe_departamento = cursor.fetchone()
            print(f"JEFE DE DEPARTAMENTO EN LA SUBDEPENDENCIA {subdep[1]}", jefe_departamento)

            if jefe_departamento:
                jefe_departamento = str(jefe_departamento[0])
                # Insertar el nodo del departamento en la tabla "nodos"
                if jefe_departamento:
                    nombre_departamento = f"{subdep[1]}.\n(Jefe {jefe_departamento})"
                else:
                    nombre_departamento = subdep[1]
            else:
                nombre_departamento = subdep[1]

            subdep_id, subdep_nombre = subdep

            # Insertar el nodo de la subdependencia en la tabla "nodos"
            cursor.execute("INSERT INTO nodos (id, nombre, tipo) VALUES (?, ?, ?)",
                           (subdep_id, nombre_departamento, "Subdependencia"))
            # Insertar la relación entre el nodo padre y el nodo hijo en la tabla "aristas"
            cursor.execute("INSERT INTO aristas (nodo_padre_id, nodo_hijo_id) VALUES (?, ?)",
                           (nodo_padre_id, subdep_id))
            insertar_subdependencias(subdep_id, subdep_id)  # Llamar recursivamente para las subdependencias

    insertar_subdependencias(dependencia_id, dependencia_id)

    organigrama = graphviz.Digraph(node_attr={'color': 'lightblue2', 'style': 'filled', 'shape': 'box'},
                                   edge_attr={'color': 'darkgreen', 'arrowhead': 'vee', 'splines': 'ortho'})

    directorio_temporal = os.path.join(os.path.expanduser("~"), "temp")
    os.makedirs(directorio_temporal, exist_ok=True)

    def generar_relaciones():
        """
        Genera las relaciones entre los nodos en el organigrama.
        Obtiene las relaciones de la base de datos y establece las conexiones en el organigrama.
        """
        relaciones = cursor.execute("""SELECT p.nombre AS departamento_padre, h.nombre AS departamento_hijo
                                        FROM aristas a
                                        JOIN nodos p ON a.nodo_padre_id = p.id
                                        JOIN nodos h ON a.nodo_hijo_id = h.id;""")
        for ph in relaciones:
            padre = ph[0]
            hijo = ph[1]
            organigrama.edge(padre, hijo)

    generar_relaciones()

    ruta_archivo = os.path.join(directorio_temporal, "organigrama")
    organigrama.render(ruta_archivo, format='jpg', view=True)

    # Eliminar los nodos y las aristas guardados en la base de datos
    cursor.execute("DELETE FROM nodos;")
    cursor.execute("DELETE FROM aristas;")
    conn.commit()
    Regresar_A_Inicio(org_id)

