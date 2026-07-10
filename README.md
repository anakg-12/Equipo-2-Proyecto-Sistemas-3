# SmartGym API
## Caracteristicas Principales
Sistema de Backend asíncrono para la gestión automatizada, control de acceso, membresías de gimnasios y mucho mas. Desarrollado como proyecto.

## Tecnologias Utilizadas

| Área               | Tecnologías                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| Backend            | Python 3.13, FastAPI, SQLAlchemy 2.0 (asyncio), Pydantic                    |
| Base de datos      | PostgreSQL, asyncpg                                                         |
| Seguridad          | PyJWT, argon2-cffi                                                          |
| Middleware         | Logging personalizado                                                       |

## Configuración e Instalación
Requisitos previos:
Python 3.13 (sin Docker)
PostgreSQL (sin Docker)
Docker Desktop (con Docker)
Clonar repositorio:
* **git clone:** 
```bash
https://github.com/laboratorio-1-2026-1/lab1-proyecto-2026-1-30266566-31089011-31099867.git
```
* **Variables de entorno:** Crea un archivo .env en la raíz del proyecto siguiendo el ejemplo de .env.example

### Sin Docker:

* **Instalacion de dependencias:** 
```bash
pip install -r requirements.txt

```
* **Crear la base de datos:**
Conéctate a PostgreSQL y ejecuta:
```bash
CREATE DATABASE smartgym;
```
* **Crear las tablas y cargar datos iniciales:**
```bash
python -c "from app.bd.database import async_engine, Base; import asyncio; asyncio.run(async_engine.begin().run_sync(Base.metadata.create_all))"
python seed.py
```
* **Ejecución de la Aplicación:** 
```bash
uvicorn app.main:app --reload

```
### Con docker:
* **Instala docker:** 
```bash
https://docs.docker.com/desktop/setup/install/windows-install/
```
* **Configuración de líneas (Solo Windows):**
> ⚠️ **Importante:** Antes de correr el contenedor, abre el archivo `entrypoint.sh` en VS Code. En la esquina inferior derecha de la barra de estado, haz clic donde dice **CRLF** y cámbialo a **LF** para evitar errores de ejecución en Linux.

* **ejecutar:**
```bash
docker compose up --build
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

