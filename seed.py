import asyncio
from datetime import datetime, date, timedelta, time
from app.bd.database import AsyncSessionLocal
from app.models import (
    RolModel,
    UsuarioModel,
    CategoriaMaquinaModel,
    MaquinaModel,
    PlanSuscripcionModel,
    ProductoTiendaModel,
    ClienteModel,
    EntrenadorModel,
    DisciplinaModel,
    MembresiaClienteModel,
    PagoFacturaModel,
    SesionProgramadaModel,
    ReservaInscripcionModel,
)
from app.core.security import hash_password
from sqlalchemy import select
from app.constants import MachineStatus, MembershipState, SessionState, ReservationState, ProductCategory, PayMethod


async def seed():
    async with AsyncSessionLocal() as db:
        # 1.Roles
        roles_data = [
            {"nombre": "Administracion", "descripcion": "Acceso total al sistema"},
            {"nombre": "Finanzas", "descripcion": "Gestión de pagos y reportes"},
            {
                "nombre": "Entrenadores",
                "descripcion": "Gestión de clases y evaluaciones",
            },
            {"nombre": "Clientes", "descripcion": "Acceso a reservas"},
        ]
        for r in roles_data:
            exists = await db.execute(
                select(RolModel).where(RolModel.nombre == r["nombre"])
            )
            if not exists.scalar_one_or_none():
                db.add(RolModel(**r))
        await db.commit()
        print("roles creados")

        # Obtener IDs de roles (para referencia)
        roles = {}
        for nombre in ["Administracion", "Finanzas", "Entrenadores", "Clientes"]:
            result = await db.execute(select(RolModel).where(RolModel.nombre == nombre))
            roles[nombre] = result.scalar_one().rol_id

        # Usuarios finanzas y administracion de ejemplo
        admins_data = [
            {
                "username": "admin",
                "email": "admin@smartgym.com",
                "password": "admin123",
                "nombre": "Admin",
                "apellido": "Principal",
                "cedula": "000",
                "rol": "Administracion",
            },
            {
                "username": "finanzas1",
                "email": "finanzas@smartgym.com",
                "password": "finanzas123",
                "nombre": "Luis",
                "apellido": "García",
                "cedula": "001",
                "rol": "Finanzas",
            },
        ]
        for a in admins_data:
            exists = await db.execute(
                select(UsuarioModel).where(UsuarioModel.email == a["email"])
            )
            if not exists.scalar_one_or_none():
                user = UsuarioModel(
                    username=a["username"],
                    email=a["email"],
                    password_hash=hash_password(a["password"]),
                    nombre=a["nombre"],
                    apellido=a["apellido"],
                    cedula=a["cedula"],
                    rol_id=roles[a["rol"]],
                    activo=True,
                )
                db.add(user)
        await db.commit()
        print("Usuarios admin y finanzas creados")

        # 3.Clientes de ejemplo
        clientes_data = [
            {
                "username": "juan",
                "email": "juan@smartgym.com",
                "password": "cliente123",
                "nombre": "Juan",
                "apellido": "Pérez",
                "cedula": "111",
                "direccion": "Calle Siempre Viva 123",
                "fecha_nacimiento": date(1990, 5, 15),
                "telefono": "04121234567",
                "estado": True,
            },
            {
                "username": "maria",
                "email": "maria@smartgym.com",
                "password": "cliente123",
                "nombre": "María",
                "apellido": "Gómez",
                "cedula": "444",
                "direccion": "Av. Libertador 456",
                "fecha_nacimiento": date(1985, 8, 22),
                "telefono": "04127654321",
                "estado": False,
            },
            {
                "username": "pedro",
                "email": "pedro@smartgym.com",
                "password": "cliente123",
                "nombre": "Pedro",
                "apellido": "Rodríguez",
                "cedula": "333",
                "direccion": "Calle 9, Casa 12",
                "fecha_nacimiento": date(1995, 3, 10),
                "telefono": "04129876543",
                "estado": False,
            },
        ]
        for c in clientes_data:
            exists = await db.execute(
                select(UsuarioModel).where(
                    (UsuarioModel.email == c["email"])
                    | (UsuarioModel.cedula == c["cedula"])
                )
            )
            if not exists.scalar_one_or_none():
                user = UsuarioModel(
                    username=c["username"],
                    email=c["email"],
                    password_hash=hash_password(c["password"]),
                    nombre=c["nombre"],
                    apellido=c["apellido"],
                    cedula=c["cedula"],
                    rol_id=roles["Clientes"],
                    activo=c["estado"],
                )
                db.add(user)
                await db.flush()
                cliente_ext = ClienteModel(
                    usuario_id=user.usuario_id,
                    direccion=c["direccion"],
                    fecha_nacimiento=c["fecha_nacimiento"],
                    telefono=c["telefono"],
                    activo=c["estado"],
                )
                db.add(cliente_ext)
        await db.commit()
        print("Clientes de ejemplo creados")

        # 4. Entrenadores de ejemplo
        entrenadores_data = [
            {
                "username": "carlos",
                "email": "carlos@smartgym.com",
                "password": "entrenador123",
                "nombre": "Carlos",
                "apellido": "López",
                "cedula": "222",
                "especialidad": "Crossfit y Musculación",
                "telefono": "04141234567",
            },
            {
                "username": "laura",
                "email": "laura@smartgym.com",
                "password": "entrenador123",
                "nombre": "Laura",
                "apellido": "Martínez",
                "cedula": "555",
                "especialidad": "Pilates y Yoga",
                "telefono": "04149876543",
            },
        ]
        for e in entrenadores_data:
            exists = await db.execute(
                select(UsuarioModel).where(
                    (UsuarioModel.email == e["email"])
                    | (UsuarioModel.cedula == e["cedula"])
                )
            )
            if not exists.scalar_one_or_none():
                user = UsuarioModel(
                    username=e["username"],
                    email=e["email"],
                    password_hash=hash_password(e["password"]),
                    nombre=e["nombre"],
                    apellido=e["apellido"],
                    cedula=e["cedula"],
                    rol_id=roles["Entrenadores"],
                    activo=True,
                )
                db.add(user)
                await db.flush()
                entrenador_ext = EntrenadorModel(
                    usuario_id=user.usuario_id,
                    especialidad=e["especialidad"],
                    telefono=e["telefono"],
                    activo=True,
                )
                db.add(entrenador_ext)
        await db.commit()
        print("Entrenadores de ejemplo creados")

        # 4.5 Disciplinas de ejemplo
        disciplinas_data = [
            {
                "nombre": "Jumping",
                "descripcion": "Clase aeróbica de alta instensidad realizada en un mini tramppolín",
            },
            {
                "nombre": "Pilates",
                "descripcion": "Clase de acondicionamiento físico, respiración y flexibilidad",
            },
            {
                "nombre": "Crossfit",
                "descripcion": "Entrenamiento funcional de alta intensidad",
            },
        ]

        for disc in disciplinas_data:
            exists = await db.execute(
                select(DisciplinaModel).where(DisciplinaModel.nombre == disc["nombre"])
            )
            if not exists.scalar_one_or_none():
                db.add(DisciplinaModel(**disc))

        await db.commit()
        print("Disciplinas de ejemplo creadas")

        # 4.Categorias de máquinas
        categorias_data = [
            {
                "nombre": "Cardiovascular",
                "descripcion": "Máquinas de cardio (cintas, elípticas)",
            },
            {"nombre": "Musculación", "descripcion": "Máquinas de fuerza guiada"},
            {"nombre": "Peso Libre", "descripcion": "Barras, mancuernas, discos"},
        ]
        for cat in categorias_data:
            exists = await db.execute(
                select(CategoriaMaquinaModel).where(
                    CategoriaMaquinaModel.nombre == cat["nombre"]
                )
            )
            if not exists.scalar_one_or_none():
                db.add(CategoriaMaquinaModel(**cat))
        await db.commit()
        print("Categorías de máquinas creadas")

        # Obtener IDs de categorías
        cat_ids = {}
        for cat in categorias_data:
            result = await db.execute(
                select(CategoriaMaquinaModel).where(
                    CategoriaMaquinaModel.nombre == cat["nombre"]
                )
            )
            cat_ids[cat["nombre"]] = result.scalar_one().categoria_id

        # 5. Máquinas de ejemplo
        maquinas_data = [
            {
                "nombre": "Cinta de correr T-3000",
                "descripcion_tecnica": "Motor",
                "estado_operativo": MachineStatus.activa.value,
                "categoria_id": cat_ids["Cardiovascular"],
                "fecha_compra": datetime(2024, 1, 15).date(),
            },
            {
                "nombre": "Bicicleta T-800",
                "descripcion_tecnica": "Volante",
                "estado_operativo": MachineStatus.activa.value,
                "categoria_id": cat_ids["Cardiovascular"],
                "fecha_compra": datetime(2024, 2, 10).date(),
            },
            {
                "nombre": "Máquina de pecho",
                "descripcion_tecnica": "Prensa de pecho sentado, ajustable",
                "estado_operativo": MachineStatus.activa.value,
                "categoria_id": cat_ids["Musculación"],
                "fecha_compra": datetime(2023, 12, 5).date(),
            },
            {
                "nombre": "Jaula de sentadillas",
                "descripcion_tecnica": "Jaula multifuncional con barra",
                "estado_operativo": MachineStatus.activa.value,
                "categoria_id": cat_ids["Peso Libre"],
                "fecha_compra": datetime(2024, 3, 20).date(),
            },
            {
                "nombre": "Mancuernas",
                "descripcion_tecnica": "Set de mancuernas con discos",
                "estado_operativo": MachineStatus.activa.value,
                "categoria_id": cat_ids["Peso Libre"],
                "fecha_compra": datetime(2024, 4, 1).date(),
            },
        ]
        for m in maquinas_data:
            exists = await db.execute(
                select(MaquinaModel).where(MaquinaModel.nombre == m["nombre"])
            )
            if not exists.scalar_one_or_none():
                db.add(MaquinaModel(**m))
        await db.commit()
        print("5 máquinas de ejemplo creadas")

        # 6. Planes de suscripción
        planes_data = [
            {
                "nombre": "Mensual Basico",
                "descripcion": "Acceso 30 días",
                "duracion_dias": 30,
                "costo": 30.0,
                "tipo": "mensual",
                "activo": True,
            },
            {
                "nombre": "Anual",
                "descripcion": "Acceso a 365 dias",
                "duracion_dias": 365,
                "costo": 200.0,
                "tipo": "anual",
                "activo": True,
            },
            {
                "nombre": "Pase Diario",
                "descripcion": "Acceso por 1 día",
                "duracion_dias": 1,
                "costo": 5.0,
                "tipo": "diario",
                "activo": True,
            },
        ]
        for p in planes_data:
            exists = await db.execute(
                select(PlanSuscripcionModel).where(
                    PlanSuscripcionModel.nombre == p["nombre"]
                )
            )
            if not exists.scalar_one_or_none():
                db.add(PlanSuscripcionModel(**p))
        await db.commit()
        print("Planes de suscripción creados")

        # Obtener IDs de planes (para membresías)
        planes = {}
        for plan in planes_data:
            result = await db.execute(
                select(PlanSuscripcionModel).where(
                    PlanSuscripcionModel.nombre == plan["nombre"]
                )
            )
            planes[plan["nombre"]] = result.scalar_one().plan_id

        # Obtener clientes
        clientes_db = {}
        for cliente in clientes_data:
            user = await db.execute(
                select(UsuarioModel).where(UsuarioModel.email == cliente["email"])
            )
            user_obj = user.scalar_one_or_none()
            if user_obj:
                cliente_model = await db.execute(
                    select(ClienteModel).where(
                        ClienteModel.usuario_id == user_obj.usuario_id
                    )
                )
                clientes_db[cliente["username"]] = cliente_model.scalar_one_or_none()

        # Membresías para cada cliente
        membresias_data = [
            {
                "cliente_username": "juan",
                "plan_nombre": "Mensual Basico",
                "fecha_inicio": date.today(),
                "estado": MembershipState.activa.value,
            },
            {
                "cliente_username": "maria",
                "plan_nombre": "Anual",
                "fecha_inicio": date.today() - timedelta(days=10),
                "estado": MembershipState.inactiva.value,
            },
        ]
        for mem in membresias_data:
            cliente = clientes_db.get(mem["cliente_username"])
            plan_id = planes.get(mem["plan_nombre"])
            if cliente and plan_id:
                plan = (
                    await db.execute(
                        select(PlanSuscripcionModel).where(
                            PlanSuscripcionModel.plan_id == plan_id
                        )
                    )
                ).scalar_one()
                duracion = plan.duracion_dias
                fecha_inicio = mem["fecha_inicio"]
                fecha_fin = fecha_inicio + timedelta(days=duracion - 1)
                # Verificar si ya existe membresía activa similar
                exists = await db.execute(
                    select(MembresiaClienteModel).where(
                        MembresiaClienteModel.cliente_id == cliente.cliente_id,
                        MembresiaClienteModel.fecha_inicio == fecha_inicio,
                    )
                )
                if not exists.scalar_one_or_none():
                    nueva_membresia = MembresiaClienteModel(
                        cliente_id=cliente.cliente_id,
                        plan_id=plan_id,
                        fecha_inicio=fecha_inicio,
                        fecha_fin=fecha_fin,
                        estado=mem["estado"],
                    )
                    db.add(nueva_membresia)
                    await db.flush()

                    # Evaluamos directamente el atributo real del diccionario
                    if mem["estado"] == MembershipState.activa.value:
                        pago = PagoFacturaModel(
                            membresia_id=nueva_membresia.membresia_id,
                            monto=plan.costo,
                            fecha_pago=fecha_inicio,
                            metodo_pago=(
                                PayMethod.efectivo.value
                                if mem["cliente_username"] == "juan"
                                else "Tarjeta"
                            ),
                            referencia=f"SEED_{mem['cliente_username'].upper()}",
                        )
                        db.add(pago)

        await db.commit()
        print("Membresías y pagos creados")

        # 7. Productos de tienda
        productos_data = [
            {
                "nombre": "Botella deportiva",
                "descripcion": "Botella de acero inoxidable 750ml",
                "precio": 8.0,
                "stock": 50,
                "categoria": ProductCategory.accesorios.value,
            },
            {
                "nombre": "Toalla de microfibra",
                "descripcion": "Toalla absorbente",
                "precio": 5.0,
                "stock": 30,
                "categoria": ProductCategory.accesorios.value,
            },
            {
                "nombre": "Proteína en polvo",
                "descripcion": "2lb, sabor chocolate",
                "precio": 35.0,
                "stock": 20,
                "categoria": ProductCategory.suplementos.value,
            },
        ]
        for prod in productos_data:
            exists = await db.execute(
                select(ProductoTiendaModel).where(
                    ProductoTiendaModel.nombre == prod["nombre"]
                )
            )
            if not exists.scalar_one_or_none():
                db.add(ProductoTiendaModel(**prod))
        await db.commit()
        print("Productos de tienda creados")

        # 8. Sesiones programadas de ejemplo
        # Obtener disciplinas y entrenadores
        disciplinas = {}
        for disc in disciplinas_data:
            result = await db.execute(
                select(DisciplinaModel).where(DisciplinaModel.nombre == disc["nombre"])
            )
            disciplinas[disc["nombre"]] = result.scalar_one().disciplina_id

        entrenadores_db = {}
        for ent in entrenadores_data:
            user = await db.execute(
                select(UsuarioModel).where(UsuarioModel.email == ent["email"])
            )
            user_obj = user.scalar_one_or_none()
            if user_obj:
                ent_model = await db.execute(
                    select(EntrenadorModel).where(
                        EntrenadorModel.usuario_id == user_obj.usuario_id
                    )
                )
                entrenadores_db[ent["username"]] = ent_model.scalar_one_or_none()

        sesiones_data = [
            {
                "disciplina": "Crossfit",
                "entrenador_username": "carlos",
                "fecha_hora_inicio": datetime.combine(
                    date.today() + timedelta(days=3), time(hour=10), tzinfo=None
                ),
                "fecha_hora_fin": datetime.combine(
                    date.today() + timedelta(days=3), time(hour=11), tzinfo=None
                ),
                "cupo_maximo": 15,
                "ubicacion": "Sala 1",
                "nombre": "Clase General",
            },
            {
                "disciplina": "Pilates",
                "entrenador_username": "laura",
                "fecha_hora_inicio": datetime.combine(
                    date.today() + timedelta(days=3), time(hour=9), tzinfo=None
                ),
                "fecha_hora_fin": datetime.combine(
                    date.today() + timedelta(days=3), time(hour=10), tzinfo=None
                ),
                "cupo_maximo": 12,
                "ubicacion": "Sala 2",
                "nombre": "Clase General",
            },
        ]
        for ses in sesiones_data:
            exists = await db.execute(
                select(SesionProgramadaModel).where(
                    SesionProgramadaModel.disciplina_id
                    == disciplinas[ses["disciplina"]],
                    SesionProgramadaModel.fecha_hora_inicio == ses["fecha_hora_inicio"],
                )
            )
            if not exists.scalar_one_or_none():
                nueva_sesion = SesionProgramadaModel(
                    disciplina_id=disciplinas[ses["disciplina"]],
                    entrenador_id=entrenadores_db[
                        ses["entrenador_username"]
                    ].entrenador_id,
                    fecha_hora_inicio=ses["fecha_hora_inicio"],
                    fecha_hora_fin=ses["fecha_hora_fin"],
                    cupo_maximo=ses["cupo_maximo"],
                    ubicacion=ses["ubicacion"],
                    nombre=ses["nombre"],
                    estado=SessionState.programada.value,
                )
                db.add(nueva_sesion)
        await db.commit()
        print("Sesiones programadas creadas")

        # Reservas
        # Obtener sesiones creadas y clientes
        sesiones_db = await db.execute(select(SesionProgramadaModel))
        sesiones_list = sesiones_db.scalars().all()
        for ses in sesiones_list:
            # Reservas para clientes (solo algunos)
            for cliente_username, cliente_obj in clientes_db.items():
                if cliente_username in ["juan"]:
                    exists = await db.execute(
                        select(ReservaInscripcionModel).where(
                            ReservaInscripcionModel.cliente_id
                            == cliente_obj.cliente_id,
                            ReservaInscripcionModel.sesion_id == ses.sesion_id,
                        )
                    )
                    if not exists.scalar_one_or_none():
                        reserva = ReservaInscripcionModel(
                            cliente_id=cliente_obj.cliente_id,
                            sesion_id=ses.sesion_id,
                            estado=ReservationState.activa.value,
                        )
                        db.add(reserva)
        await db.commit()
        print("Reservas de ejemplo creadas")


if __name__ == "__main__":
    asyncio.run(seed())
