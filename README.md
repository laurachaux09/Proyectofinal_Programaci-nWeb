# Gimnasio Corlau — Sistema Integral de Gestión

Aplicación web desarrollada en **Python (Flask)** y **PostgreSQL** para la administración operativa de un gimnasio, implementando operaciones CRUD completas sobre un modelo relacional normalizado hasta la Tercera Forma Normal (3FN)


## Integrantes
* Laura Sofía Chaux Trujillo
* Miguel Ángel Cortés


## Descripción del proyecto

Gimnasio Corlau es una aplicación web diseñada para facilitar la administración de las operaciones de un gimnasio mediante una plataforma centralizada.

El sistema permite realizar operaciones CRUD (crear, consultar, actualizar y eliminar o desactivar registros) sobre los diferentes módulos, además de gestionar las relaciones entre las entidades y validar la información mediante restricciones en PostgreSQL.


## Tecnologías utilizadas

- *Python:* lenguaje de programación utilizado para la lógica del sistema.
- *Flask:* framework utilizado para desarrollar la aplicación web.
- *PostgreSQL:* sistema gestor de bases de datos.
- *Psycopg2:* conexión entre Python y PostgreSQL.
- *HTML5 y CSS3:* estructura y estilos de las páginas.
- *Bootstrap 5:* diseño adaptable e interfaz visual.
- *Jinja2:* generación dinámica de las plantillas HTML.
- *python-dotenv:* gestión de variables de entorno.

## Módulos del sistema

El proyecto cuenta con los siguientes módulos:

1. *Socios:* registro, consulta, edición y desactivación de socios.
2. *Entrenadores:* administración de los entrenadores del gimnasio.
3. *Especialidades:* gestión de las disciplinas y áreas de entrenamiento.
4. *Entrenador - Especialidad:* asignación de especialidades a los entrenadores.
5. *Planes de membresía:* administración de planes, precios y duraciones.
6. *Membresías:* gestión de las membresías contratadas por los socios.
7. *Pagos:* registro y administración de los pagos de las membresías.
8. *Clases:* programación y administración de clases grupales.
9. *Inscripciones a clases:* registro y control de las inscripciones de los socios.

## Estructura del proyecto

text
Gimnasio_CorLau/
│
├── app.py
├── config.py
├── db.py
├── routes/
│   ├── __init__.py
│   ├── socios.py
│   ├── entrenadores.py
│   ├── especialidades.py
│   ├── planes_membresia.py
│   ├── entrenadores_especialidades.py
│   ├── membresias.py
│   ├── pagos.py
│   ├── clases.py
│   └── inscripciones_clase.py
│
├── templates/
├── static/
├── database/
├── docs/
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md


## Requisitos previos

Antes de ejecutar el proyecto, es necesario tener instalado:

- Python 3.
- PostgreSQL.
- Visual Studio Code (recomendado).
- Git (opcional, para clonar el repositorio).

## Instalación y configuración

### 1. Clonar el repositorio

Abrir una terminal y ejecutar:

bash
git clone https://github.com/laurachaux09/Proyectofinal_Programaci-nWeb


Ingresar a la carpeta del proyecto:

bash
cd Gimnasio_CorLau

### 2. Crear el entorno virtual

En Windows, ejecutar:

powershell
python -m venv .venv


Activar el entorno virtual:

powershell
.venv\Scripts\Activate


### 3. Instalar las dependencias

Con el entorno virtual activado, ejecutar:

bash
python -m pip install -r requirements.txt


### 4. Configurar PostgreSQL

1. Abrir PostgreSQL mediante pgAdmin.
2. Crear una base de datos llamada gimnasio_db.
3. Ejecutar el script SQL de creación de tablas ubicado en la carpeta database/.
4. Ejecutar el script de inserción de datos para cargar los registros iniciales, si se encuentra disponible.

### 5. Configurar las variables de entorno

Crear un archivo .env en la raíz del proyecto, tomando como referencia el archivo .env.example.

Configurar en él los datos de conexión a PostgreSQL, de acuerdo con las variables utilizadas en config.py.

*Importante:* el archivo .env contiene información de configuración privada y no debe subirse al repositorio.

### 6. Ejecutar la aplicación
Con el entorno virtual activado y PostgreSQL disponible, ejecutar:

bash
python app.py


Abrir en el navegador la dirección local que indique Flask en la terminal, normalmente:

text
http://127.0.0.1:5000/

La carpeta database/ contiene los archivos relacionados con la creación, carga y respaldo de la base de datos.

## Consideraciones

- Es necesario tener PostgreSQL instalado y en funcionamiento para utilizar la aplicación.
- La base de datos debe estar creada y configurada antes de iniciar Flask.
- Las credenciales de conexión deben configurarse en el archivo .env.
- El entorno virtual .venv/ no se incluye en el repositorio.
- El archivo .env no se incluye por motivos de seguridad.
