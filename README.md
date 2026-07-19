# SmartGym API
## Características Principales
Sistema de Backend asíncrono para la gestión automatizada, control de acceso, membresías de gimnasios y mucho más. Desarrollado como proyecto.

## Tecnologías Utilizadas

| Área               | Tecnologías                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| Backend            | Python 3.13, FastAPI, SQLAlchemy 2.0 (asyncio), Pydantic                    |
| Base de datos      | PostgreSQL, asyncpg                                                         |
| Seguridad          | PyJWT, argon2-cffi                                                          |
| Middleware         | Logging personalizado                                                       |

## Configuración e Instalación
Requisitos previos:
- Python 3.13 (sin Docker)
- PostgreSQL (sin Docker)
- Docker Desktop (con Docker)
* **Clonar repositorio:** 
```bash
git clone https://github.com/anakg-12/Equipo-2-Proyecto-Sistemas-3.git
```
* **Variables de entorno:** Crea un archivo .env en la raíz del proyecto siguiendo el ejemplo de .env.example.

### Sin Docker:

* **Crear entorno virtual** 
```bash 
python -m venv .venv  
```
* **Activar entorno** 
* * **Windows:** 
```bash
.venv\Scripts\activate 
```
* * **Mac/Linux:** 
```bash 
source .venv/bin/activate 
```

* **Instalación de dependencias:** 
```bash
pip install -r requirements.txt

```
* **Crear la base de datos:**
Conéctate a PostgreSQL y ejecuta:
```bash
CREATE DATABASE smartgym;
```
* **Crear las tablas y cargar datos iniciales:** Ejecute el siguiente script para inicializar la base de datos y llenarla con los datos iniciales.
```bash
python init_and_seed.py
```

> ⚠️ **Advertencia:** Al ejecutar el script de datos semilla se borrarán las tablas existentes en la base de datos junto con los datos que contengan (si existen previamente) y luego creará las tablas de forma automática con los datos iniciales. No ejecute el script de datos semilla si, luego de la creación inicial, ha registrado información que no desea perder.

* **Ejecución de la Aplicación:** 
```bash
uvicorn app.main:app --reload

```
### Con docker:
* **Instala docker:** Acceda a la siguiente URL para instalar Docker Desktop en su equipo.
```bash
https://docs.docker.com/desktop/setup/install/windows-install/
```
* **Configuración de líneas (Solo Windows):**
> ⚠️ **Importante:** Antes de correr el contenedor, abre el archivo `entrypoint.sh` en VS Code. En la esquina inferior derecha de la barra de estado, haz clic donde dice **CRLF** y cámbialo a **LF** para evitar errores de ejecución en Linux.

* **Ejecutar:** Para levantar los contenedores del proyecto.
```bash
docker compose up --build
```

* **Detener contenedores:** Para detener la ejecución del proyecto con Docker y limpiar su entorno local, ejecute el siguiente comando.
```bash
docker compose down
```

## Documentación de la API
Swagger UI: 
```bash
http://localhost:8000/docs
```
## Autores
* **Daniela Sofia Marquez**
* **Tomas David Soto** 
* **Ana Karina Garcia**
* **Nelson Hernández**
* **Jeiker David Morales**
* **Carlos Paradas**
* **Yosger Toro**
* **Ricardo González**
