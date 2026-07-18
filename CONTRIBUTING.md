# Guía de Contribución y Flujo de Trabajo
## Bienvenida y Propósito de la Guía

Estimado colega, te damos la bienvenida al presente proyecto backend desarrollado para la gestión integral del gimnasio SmartGym.

En las siguientes secciones se presentan las reglas que rigen el trabajo colaborativo para el desarrollo del proyecto, así como el flujo de trabajo vigente entre los equipos y las herramientas utilizadas por cada participante.

Para conocer detalles sobre los requisitos funcionales y no funcionales que cubre el proyecto, su alcance, el stack tecnológico completo utilizado, el diseño de la base de datos y los endpoints implementados, así como los datos necesarios para probar el sistema, por favor comunicate con el líder del proyecto o el responsable de contratación para que te sea entregada la documentación completa del proyecto (en formato PDF).

Cabe destacar que esta guía se ofrece para hacer del conocimiento general los estándares que rigen el trabajo colaborativo y las herramientas empleadas para ello. **No pretende ser indicativo de una naturaleza "open source"** propia del sistema, ya que la contratación de todos los colaboradores debe ser explícita para participar en el desarrollo actual.

## Herramientas Utilizadas en el Flujo de Trabajo

- **Git y GitHub:** Creación de ramas para solucionar errores, implementar funcionalidades y plataforma para contener, administrar y mantener el avance técnico del proyecto.
- **Jira Software (Atlassian):** Plataforma web para coordinar la asignación, ejecución y revisión de las actividades entre equipos, siguiendo la metodología Scrum. 

## Instalación y Ejecución del Proyecto

Los aspectos concernientes a la instalación, configuración y ejecución del proyecto, ya sea desde su entorno local o utilizando Docker, se encuentran detallados en el README integrado al proyecto. Consulte la [ guía inicial del README ](./README.md) para ver las instrucciones de instalación.

## Equipos de Trabajo y Responsabilidades

Para cubrir las diferentes necesidades técnicas del sistema, asegurar una distribución uniforme del trabajo y separar las responsabilidades según las destrezas de los participantes, existen tres grupos enfocados en las tres áreas más importantes del proyecto:

1. **Lógica de Negocio y Seguridad:** Centrados en el flujo comercial y operativo del sistema, la implementación de reglas de negocio críticas y la eliminación de brechas de seguridad.

2. **Infraestructura, Base de Datos y DevOps:** Orientados al diseño y modelado de la capa de datos, infraestructura y contenerización del proyecto.

3. **Código Limpio (Clean Code):** Dedicados a la estandarización, aseguramiento de la calidad y arquitectura limpia del repositorio, facilitando la mantenibilidad del sistema.

## Flujo de Trabajo con Git y Estándares de Uso

A continuación, se presentan las reglas que rigen el flujo de trabajo y colaboración con Git y GitHub, así como su integración con la plataforma web Jira:

1. **Asignación de Tareas con Jira:** Las tareas son creadas a través de Jira, agrupadas en catálogos denominados **Épicas** y asignados a los líderes responsables de cada equipo de trabajo. Es responsabilidad del líder de equipo asignar las tareas de su épica correspondiente a los integrantes de su equipo y monitorear su progreso.

2. **Detalles de Tarea:** Cada tarea o incidencia creada en Jira contiene: una historia de usuario, que contextualiza el problema a resolver; criterios de aceptación, los requisitos mínimos que debe cubrir la solución; rama Git obligatoria, el nombre de la rama de Git que el desarrollador responsable de la incidencia deberá crear en su entorno local para solucionar el incoveniente.

3. **Creación de Rama Local Aislada y Protocolo de Publicación:** Cada desarrollador debe crear una rama local dedicada a su asignación siguiendo la nomenclatura especificada en Jira, **partiendo siempre de la rama develop**. Queda terminantemente prohibido subir cambios directos a las ramas "main" o "develop" y crear nombres propios de ramas distintos a los asignados en Jira. En el momento en que el desarrollador inicie la resolución de la incidencia, deberá ingresar a Jira y cambiar el estado de la tarjeta de "Por hacer" a "En curso".

4. **Protocolo de Publicación:** Antes de subir la rama local al servidor remoto (GitHub), el desarrollador está en la obligación de actualizar su entorno para absorber los cambios que otros compañeros hayan integrado previamente. Para ello, deberá ejecutar un arrastre (pull) de la rama de desarrollo hacia su rama de trabajo local. Será responsabilidad del desarrollador resolver en su máquina local los conflictos que genere el Pull previo y asegurar que el proyecto funcione antes de proseguir. Una vez sincronizada la rama local con develop y resueltos los eventuales conflictos, el programador subirá su rama aislada al repositorio remoto en GitHub. Una vez culminado el desarrollo, verificado el funcionamiento local y subida la rama al repositorio remoto, el desarrollador abrirá un Pull Request (PR) en GitHub apuntando hacia la rama develop. **El desarrollador NO modificará el estado del ticket en Jira**. Lo único que deberá hacer es cambiar el campo de "Persona asignada", transfiriendo el ticket directamente al líder de su Épica.

## Protocolo de Integración de Cambios con GitHub

Finalmente, se presenta el protocolo de integración de cambios (a través de los Pull Request) que debe seguirse en GitHub:

1. **Creción del Pull Request (PR):** Tras subir la rama a GitHub, el desarrollador abrirá un Pull Request apuntando estrictamente hacia la rama develop (nunca hacia main). El PR deberá cumplir con la siguiente estructura de presentación:
- - **Título del PR:** Debe incluir el identificador del ticket en Jira y el nombre formal de la tarea (Ejemplo: [SEC-01] Validar usuario activo en el servicio de login).
- - **Descripción del PR:** Debe detallar de forma precisa: (1) El fallo que se está solucionando, (2) Los archivos del sistema que fueron modificados, y (3) La evidencia o método de prueba (ej. captura de Postman o log de terminal) que demuestra que la solución funciona y no rompe el entorno.

2. **Revisión y Fusión (Code Review):** Ningún desarrollador puede autoprobar o fusionar (merge) su propio Pull Request. La integración a develop será ejecutada únicamente por el responsable de épica, tras auditar el código y verificar que cumpla con los criterios de aceptación.

3. **Fase de Auditoría:** Al recibir la notificación de asignación del ticket, el Líder de Épica asumirá el control de la incidencia y cambiará su estado en Jira a "En revisión" mientras procede a auditar el código y evaluar el Pull Request en GitHub.

4. **Cierre de PR:** El responsable de Épica evaluará los cambios sometidos y emitirá uno de los siguientes dictámenes:

- - **Aprobación y Cierre (Finalizado):** Si el código cumple con los criterios de aceptación y no genera regresiones, el líder de Épica aprobará (Approve) y fusionará (Merge) el Pull Request hacia la rama develop. Inmediatamente después de la fusión, el líder eliminará la rama del repositorio remoto en GitHub (y el desarrollador deberá eliminarla de su entorno local) para mantener la pulcritud del repositorio. Finalmente, el líder cambiará el estado de la tarjeta en Jira a "Finalizado".

- - **Rechazo por Incidencias (QA Reject):** Si el Pull Request presenta errores de compilación, fallos en la lógica o no cumple con el requerimiento, el líder de Épica solicitará cambios en GitHub detallando las correcciones necesarias. En Jira, el líder marcará la incidencia bajo el estatus o etiqueta de "QA Reject" (Rechazo de Calidad) y devolverá el ticket al estado "En curso" Reasignará la tarjeta nuevamente al desarrollador original para que aplique las correcciones solicitadas en la misma rama de trabajo y repita el ciclo de revisión.
