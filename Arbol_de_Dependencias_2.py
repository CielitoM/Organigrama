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


def crear_arbol(aux):
    """
    Crea un árbol de dependencias y personas a partir de un organigrama.
    Recibe un parámetro "aux" que se utiliza para identificar el organigrama.
    1. Obtiene el ID de el organigrama y lo asigna a la variable global "org_id".
    2. Busca personas con PUE = 'Director Ejecutivo' y ORG_ID = org_id.
    3. Obtiene el ID y el nombre de la dependencia raíz (DEPENDENCIA_PADRE_ID = 0).
    4. Inserta el nodo raíz en la tabla "nodos" con su nombre y tipo.
    5. Obtiene los departamentos de el organigrama.
    6. Define una función recursiva "insertar_subdependencias" para insertar nodos y aristas de las subdependencias.
    7. Inserta la raíz y los departamentos en la tabla "nodos" y "aristas".
    8. Genera el gráfico del organigrama utilizando la librería graphviz.
    9. Guarda el gráfico en un archivo y lo muestra.
    10. Elimina los nodos y las aristas guardados en la base de datos.
    11. Regresa a la función "Regresar_A_Inicio" con el parámetro org_id.

    """
    global org_id
    org_id = aux
    print(org_id)

    # Buscar personas con PUE = 'Director Ejecutivo' y ORG_ID = org_id
    cursor.execute("SELECT ID, NOM, APE FROM personas WHERE ORG_ID = ? AND PUE = 'Director Ejecutivo'", (org_id,))
    directores = cursor.fetchall()

    # Obtener el ID y el nombre de la dependencia con DEPENDENCIA_PADRE_ID = 0 y ORG_ID = org_id
    cursor.execute("SELECT ID, NOMBRE FROM dependencias WHERE DEPENDENCIA_PADRE_ID = 0 AND ORG_ID = ?", (org_id,))
    dependencia_raiz = cursor.fetchone()
    print("LA DEPENDENCIA RAIZ ES:", dependencia_raiz)

    # Insertar el nodo raíz en la tabla "nodos"
    nombre_raiz = f"{dependencia_raiz[1]}\n"
    print("NOMBRE RAIZ2:", nombre_raiz)
    if directores:
        for director in directores:
            nombre_raiz += f"Director/a {director[1]} {director[2]}\n"
    else:
        nombre_raiz = f"{dependencia_raiz[1]}\n(Sin director/es)"
        print("NOMBRE RAIZ:", nombre_raiz)

    cursor.execute("INSERT INTO nodos (id, nombre, tipo) VALUES (?, ?, ?)",
                   (dependencia_raiz[0], nombre_raiz, "Raíz"))
    print("NOMBRE RAIZ3:", nombre_raiz)

    # Obtener los departamentos
    cursor.execute("SELECT * FROM dependencias WHERE DEPENDENCIA_PADRE_ID IS NULL AND ORG_ID = ?", (org_id,))
    departamentos = cursor.fetchall()

    def insertar_subdependencias(departamento_id, nodo_padre_id, org_id):
        """
        Inserta las subdependencias de un departamento en la base de datos.
        Recibe el ID del departamento, el ID del nodo padre y el ID de el organigrama.
        Consulta la base de datos para obtener las subdependencias del departamento.
        Por cada subdependencia, obtiene el nombre y verifica si tiene un jefe de departamento.
        Inserta el nodo de la subdependencia en la tabla "nodos".
        Inserta la relación entre el nodo padre y el nodo hijo en la tabla "aristas".
        Llama recursivamente a la función para insertar las subdependencias de las subdependencias.
        """
        cursor.execute("SELECT * FROM dependencias WHERE DEPENDENCIA_PADRE_ID = ? AND ORG_ID = ?",
                       (departamento_id, org_id))
        subdependencias = cursor.fetchall()
        for subdep in subdependencias:
            subdep_id, nombre, dep_padre_id, org_id = subdep
            # Obtener el nombre del jefe de departamento si existe
            cursor.execute(
                "SELECT NOM || ' ' || APE FROM personas WHERE ORG_ID = ? AND DEP = ? AND PUE = 'Jefe de Departamento'",
                (org_id, nombre))
            jefe_departamento = cursor.fetchone()
            nombre_subdep = nombre
            if jefe_departamento:
                jefe_departamento = str(jefe_departamento[0])
                nombre_subdep += f" \n(Jefe {jefe_departamento})"
            # Insertar el nodo de la subdependencia en la tabla "nodos"
            cursor.execute("INSERT INTO nodos (id, nombre, tipo) VALUES (?, ?, ?)",
                           (subdep_id, nombre_subdep, "Subdependencia"))
            # Insertar la relación entre el nodo padre y el nodo hijo en la tabla "aristas"
            cursor.execute("INSERT INTO aristas (nodo_padre_id, nodo_hijo_id) VALUES (?, ?)",
                           (nodo_padre_id, subdep_id))
            insertar_subdependencias(subdep_id, subdep_id, org_id)  # Llamar recursivamente para las subdependencias


    # Obtener los departamentos con DEPENDENCIA_PADRE_ID = NULL
    cursor.execute("SELECT * FROM dependencias WHERE DEPENDENCIA_PADRE_ID IS NULL AND ORG_ID = ?", (org_id,))
    departamentos = cursor.fetchall()

    # Insertar la raíz y los departamentos en la tabla "nodos" y "aristas"
    for depto in departamentos:
        depto_id, nombre, dep_padre_id, org_id = depto

        # Obtener el nombre del jefe de departamento si existe
        cursor.execute(
            "SELECT NOM || ' ' || APE FROM personas WHERE ORG_ID = ? AND DEP = ? AND PUE = 'Jefe de Departamento'",
            (org_id, nombre))
        jefe_departamento = cursor.fetchone()

        if jefe_departamento:
            jefe_departamento = str(jefe_departamento[0])
            # Insertar el nodo del departamento en la tabla "nodos"
            nombre_departamento = f"{nombre}. \n(Jefe {jefe_departamento})"
        else:
            nombre_departamento = nombre
        # Insertar el nodo de la subdependencia en la tabla "nodos"
        cursor.execute("INSERT INTO nodos (id, nombre, tipo) VALUES (?, ?, ?)",
                       (depto_id, nombre_departamento, "Departamento"))

        # Insertar la relación entre el nodo padre y el nodo hijo en la tabla "aristas"
        cursor.execute("INSERT INTO aristas (nodo_padre_id, nodo_hijo_id) VALUES (?, ?)",
                       (dependencia_raiz[0], depto_id))
        insertar_subdependencias(depto_id, depto_id, org_id)  # Insertar las subdependencias

    organigrama = graphviz.Digraph(node_attr={'color': 'lightblue2', 'style': 'filled', 'shape': 'box'},
                                   edge_attr={'color': 'darkgreen', 'arrowhead': 'vee', 'splines': 'ortho'})

    directorio_temporal = os.path.join(os.path.expanduser("~"), "temp")
    os.makedirs(directorio_temporal, exist_ok=True)

    # GRAFICAR EL ARBOL
    def generar_nodos():
        """
        Genera los nodos del gráfico del organigrama.
        Consulta la base de datos para obtener los nombres de los nodos.
        Agrega cada nodo al gráfico del organigrama.
        """
        nodos = cursor.execute("""SELECT nombre FROM nodos;""")
        for nodo in nodos:
            organigrama.node(nodo[0])  # Agregar el nodo al gráfico

    def generar_relaciones():
        """
        Genera las relaciones entre departamentos y las agrega al gráfico del organigrama.
        Consulta la base de datos para obtener las relaciones existentes entre departamentos.
        Itera sobre cada relación y agrega la relación al gráfico del organigrama.
        """
        relaciones = cursor.execute("""SELECT p.nombre AS departamento_padre, h.nombre AS departamento_hijo
                                        FROM aristas a
                                        JOIN nodos p ON a.nodo_padre_id = p.id
                                        JOIN nodos h ON a.nodo_hijo_id = h.id;""")
        for ph in relaciones:
            padre = ph[0]
            hijo = ph[1]
            organigrama.edge(padre, hijo)  # Agregar la relación al gráfico

    generar_nodos()
    generar_relaciones()

    ruta_archivo = os.path.join(directorio_temporal, "organigrama")
    organigrama.render(ruta_archivo, format='jpg', view=True)

    # Eliminar los nodos y las aristas guardados en la base de datos
    cursor.execute("DELETE FROM nodos;")
    cursor.execute("DELETE FROM aristas;")
    conn.commit()
    Regresar_A_Inicio(org_id)


