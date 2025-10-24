# Sistema de Gestión de Organigramas

Un sistema completo de escritorio desarrollado en Python para crear, gestionar y visualizar organigramas empresariales con información detallada de dependencias y personal.

## Tabla de Contenidos

- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Requisitos del Sistema](#requisitos-del-sistema)
- [Instalación](#instalación)
- [Uso del Sistema](#uso-del-sistema)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Base de Datos](#base-de-datos)
- [Capturas de Pantalla](#capturas-de-pantalla)
- [Contribución](#contribución)

## Características

### Gestión de Usuarios
- Sistema de registro e inicio de sesión
- Múltiples usuarios con datos independientes
- Validación de credenciales

### Gestión de Proyectos
- Crear múltiples organigramas por usuario
- Editar información de proyectos existentes
- Eliminar proyectos con confirmación
- Copiar organigramas completos
- Filtrado por fecha de creación

### Gestión de Dependencias
- Crear estructura jerárquica ilimitada
- Agregar, modificar y eliminar departamentos
- Mover dependencias entre niveles
- Validación de integridad estructural

### Gestión de Personal
- Información completa de empleados
- Vinculación con dependencias específicas
- Datos personales y laborales
- CRUD completo de personal

### Visualización Gráfica
- Generación automática de organigramas
- Visualización completa o parcial
- Exportación en múltiples formatos
- Algoritmos optimizados de renderizado

### Reportes e Informes
- Generación de informes detallados
- Estadísticas del organigrama
- Análisis de la estructura organizacional

## 🛠 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **Tkinter**: Interfaz gráfica de usuario
- **SQLite**: Base de datos embebida
- **Pillow (PIL)**: Procesamiento de imágenes
- **tkcalendar**: Widget de calendario
- **Graphviz**: Visualización de grafos

## Requisitos del Sistema

### Software Base
- Windows 11
- Python 3.8 o superior
- Graphviz (software del sistema)

### Espacio en Disco
- Mínimo: 100 MB

## Instalación

### 1. Clonar o Descargar el Proyecto
```bash
# Si tienes git instalado
git clone [URL_DEL_REPOSITORIO]

# O descarga el archivo ZIP y extráelo
```

### 2. Crear y Activar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate.ps1
```

### 3. Instalar Dependencias de Python
```bash
# Con el entorno virtual activado
pip install Pillow tkcalendar matplotlib networkx graphviz
```

### 4. Instalar Graphviz (Software del Sistema)

#### Opción A: Usando winget (Recomendado)
```bash
winget install graphviz
```

#### Opción B: Descarga Manual
1. Visita [https://graphviz.org/download/](https://graphviz.org/download/)
2. Descarga la versión para Windows
3. Instala siguiendo las instrucciones
4. Agrega `C:\Program Files\Graphviz\bin` al PATH del sistema

### 5. Verificar Instalación
```bash
# Verificar Graphviz
dot -V

# Debería mostrar: dot - graphviz version X.X.X
```

### 6. Agregar Graphviz al PATH (si es necesario)
```bash
# Temporal (solo para la sesión actual)
$env:PATH += ";C:\Program Files\Graphviz\bin"

# Permanente: Agregar manualmente en Variables de Entorno del Sistema
```

## Uso del Sistema

### Iniciar la Aplicación
```bash
# Con el entorno virtual activado
python LOGIN.py
```

### Primera Vez - Registro
1. Ejecuta la aplicación
2. Haz clic en "Registrarse"
3. Ingresa un nombre de usuario (1-20 caracteres)
4. Ingresa una contraseña (1-20 caracteres)
5. Haz clic en "Agregar"

### Inicio de Sesión
1. Ingresa tu nombre de usuario
2. Ingresa tu contraseña
3. Haz clic en "Iniciar Sesión"

### Crear tu Primer Organigrama

#### 1. Crear Proyecto
- En la ventana principal, haz clic en "Crear"
- Ingresa el nombre del proyecto (1-25 caracteres)
- Selecciona la fecha de creación
- Haz clic en "Agregar"

#### 2. Agregar Dependencias
- Selecciona tu proyecto de la lista
- Haz clic en "Abrir Organigrama"
- Selecciona "Agregar, Modificar y Eliminar Dependencias"
- Comienza agregando la dependencia principal (ej: "Dirección General")
- Agrega subdependencias según tu estructura organizacional

#### 3. Agregar Personal
- Desde el organigrama abierto
- Selecciona "Agregar, Modificar y Eliminar Personas"
- Completa la información del empleado:
  - Cédula/ID
  - Nombre y Apellido
  - Teléfono
  - Dirección
  - Dependencia (seleccionar de la lista)
  - Salario
  - Fecha de Nacimiento
  - Puesto

#### 4. Visualizar Organigrama
- Regresa a la ventana principal
- Selecciona tu proyecto
- Haz clic en "Graficar Organigrama"
- Elige entre:
  - **Organigrama completo**: Muestra toda la estructura
  - **Desde una dependencia**: Muestra solo una rama específica

#### 5. Generar Informes
- Selecciona tu proyecto
- Haz clic en "Informes"
- Revisa las estadísticas y análisis generados

### Funciones Avanzadas

#### Copiar Organigramas
- Selecciona un proyecto existente
- Haz clic en "Copiar"
- Se creará una copia con el sufijo "- copia"

#### Editar Proyectos
- Selecciona un proyecto
- Haz clic en "Editar"
- Modifica el nombre o fecha
- Guarda los cambios

#### Mover Dependencias
- En la gestión de dependencias
- Usa la función "Mover" para reestructurar
- Selecciona la dependencia y su nueva ubicación

## Estructura del Proyecto

```
PROYECTO/
│
├── LOGIN.py                     # Punto de entrada - Autenticación
├── HOME.py                      # Ventana principal - Dashboard
├── Dependencias.py              # Gestión de departamentos/áreas
├── Personas.py                  # Gestión de personal
├── Informes.py                  # Generación de reportes
├── Arbol_de_Dependencias_1.py   # Visualización parcial
├── Arbol_de_Dependencias_2.py   # Visualización completa
│
├── organigrama.db               # Base de datos SQLite
├── logo.png                     # Logo de la aplicación
├── fondo.gif                    # Imagen de fondo
│
├── venv/                        # Entorno virtual
├── __pycache__/                 # Cache de Python
├── RESPALDO DE BASE DE DATOS/   # Respaldos de prueba
└── README.md                    # Este archivo
```

## Base de Datos

### Esquema de Tablas

#### `usuario`
- `ID`: Clave primaria autoincremental
- `NOMBRE`: Nombre de usuario (TEXT)
- `CONTRA`: Contraseña (TEXT)

#### `organigrama`
- `ID`: Clave primaria autoincremental
- `NOMBRE`: Nombre del proyecto (TEXT)
- `FECHA`: Fecha de creación (TEXT)
- `USUARIO_ID`: Referencia al usuario (INTEGER)

#### `dependencias`
- `ID`: Clave primaria autoincremental
- `NOMBRE`: Nombre de la dependencia (TEXT)
- `DEPENDENCIA_PADRE_ID`: Referencia a dependencia padre (INTEGER)
- `ORG_ID`: Referencia al organigrama (INTEGER)

#### `personas`
- `ID`: Clave primaria autoincremental
- `CED`: Cédula/Identificación (TEXT)
- `NOM`: Nombre (TEXT)
- `APE`: Apellido (TEXT)
- `TEL`: Teléfono (TEXT)
- `DIR`: Dirección (TEXT)
- `DEP`: Dependencia asignada (TEXT)
- `SAL`: Salario (TEXT)
- `NAC`: Fecha de nacimiento (TEXT)
- `PUE`: Puesto de trabajo (TEXT)
- `ORG_ID`: Referencia al organigrama (TEXT)

### Respaldos
- Se han creado respaldos en la carpeta `RESPALDO DE BASE DE DATOS/`
- Se recomienda hacer respaldos manuales periódicamente

## Capturas de Pantalla

### Ventana de Login
- Interfaz limpia con logo corporativo
- Campos de usuario y contraseña
- Opciones de registro y acceso

### Dashboard Principal
- Lista de proyectos por usuario
- Botones de acción organizados por categorías
- Información de sesión actual

### Gestión de Dependencias
- Árbol jerárquico interactivo
- Formularios de creación y edición
- Validaciones en tiempo real

### Visualización de Organigramas
- Diagramas generados automáticamente
- Múltiples formatos de exportación
- Navegación intuitiva

## Solución de Problemas Comunes

### Error: "No module named 'tkcalendar'"
```bash
pip install tkcalendar
```

### Error: "No module named 'graphviz'"
```bash
pip install graphviz
```

### Error: "graphviz executables not found"
1. Instala Graphviz del sistema: `winget install graphviz`
2. Agrega al PATH: `C:\Program Files\Graphviz\bin`
3. Verifica: `dot -V`

### La aplicación no inicia
1. Verifica que el entorno virtual esté activado
2. Confirma que todas las dependencias estén instaladas
3. Revisa que `logo.png` exista en el directorio

### Errores de base de datos
1. Verifica permisos de escritura en el directorio
2. Revisa que `organigrama.db` no esté corrupto
3. Restaura desde respaldo si es necesario



## Autor

**Maria Cielito Melgarejo Baez**

## Agradecimientos

- Comunidad de Python por las excelentes librerías
- Graphviz por la potente herramienta de visualización
- Tkinter por la interfaz gráfica multiplataforma
