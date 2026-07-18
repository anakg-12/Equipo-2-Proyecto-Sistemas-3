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

