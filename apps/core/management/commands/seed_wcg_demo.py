"""
Carga datos demo coherentes para presentación gerencial de WCG One.

Uso:
    python manage.py seed_wcg_demo
    python manage.py seed_wcg_demo --fresh   # elimina datos marcados origen=demo y re-siembra
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.core.models import (
    Contacto,
    DataImportBatch,
    Entidad,
    Producto,
    RelacionEntidadProducto,
    UnidadNegocio,
)
from apps.crm.models import Interaccion, Tarea
from apps.pgo.models import PgoTicket
from apps.risk.models import EstadoFinanciero, RiskAlerta, RiskOperacion, RiskOperationSnapshot

User = get_user_model()
DEMO_ORIGIN = "demo"


class Command(BaseCommand):
    help = "Sembra datos demo para CRM, Risk y PGO (presentación interna)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Elimina registros con origen=demo antes de sembrar de nuevo.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["fresh"]:
            self._clear_demo()
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        self.stdout.write("Sembrando datos demo WCG One...")
        unidades = self._seed_unidades()
        productos = self._seed_productos(unidades)
        entidades = self._seed_entidades()
        self._seed_contactos(entidades)
        self._seed_relaciones(entidades, productos, unidades)
        self._seed_crm(entidades, user)
        batches = self._seed_import_batches(user)
        operaciones = self._seed_risk(entidades, productos, unidades, batches.get("risk"))
        self._seed_eeff(entidades, batches.get("risk"))
        self._seed_alertas(entidades, operaciones)
        self._seed_tickets(unidades, user, batches.get("pgo"))
        self.stdout.write(
            self.style.SUCCESS(
                f"Demo OK — entidades: {Entidad.objects.filter(origen=DEMO_ORIGIN).count()}, "
                f"snapshots: {RiskOperationSnapshot.objects.count()}, "
                f"tickets: {PgoTicket.objects.filter(ticket_externo_id__startswith='TI-DEMO').count()}"
            )
        )

    def _clear_demo(self):
        PgoTicket.objects.filter(ticket_externo_id__startswith="TI-DEMO").delete()
        RiskOperationSnapshot.objects.filter(archivo_origen="demo_seed").delete()
        RiskOperacion.objects.filter(
            codigo_operacion__in=["PG01260302", "LG01260115", "FC01260288"]
        ).delete()
        RiskAlerta.objects.filter(origen=DEMO_ORIGIN).delete()
        EstadoFinanciero.objects.filter(observaciones__icontains="demo").delete()
        Interaccion.objects.filter(notas__icontains="demo").delete()
        Tarea.objects.filter(notas__icontains="demo").delete()
        DataImportBatch.objects.filter(archivo_hash__startswith="demo_seed_").delete()
        Entidad.objects.filter(origen=DEMO_ORIGIN).delete()
        self.stdout.write("Datos demo previos eliminados.")

    def _seed_unidades(self):
        data = [
            ("LEASING", "Leasing", 1),
            ("FACTORING", "Factoraje", 2),
            ("TI", "Tecnología", 3),
            ("INSURANCE", "Insurance", 4),
            ("INVESTMENT", "Inversiones", 5),
        ]
        out = {}
        for codigo, nombre, orden in data:
            obj, _ = UnidadNegocio.objects.update_or_create(
                codigo=codigo,
                defaults={"nombre": nombre, "activa": True, "orden": orden},
            )
            out[codigo] = obj
        return out

    def _seed_productos(self, unidades):
        data = [
            ("LEASING", "Leasing operativo", "LEASING"),
            ("FACTORING", "Factoraje comercial", "FACTORING"),
        ]
        out = {}
        for codigo, nombre, un_code in data:
            obj, _ = Producto.objects.update_or_create(
                codigo=codigo,
                defaults={"nombre": nombre, "activo": True},
            )
            out[codigo] = obj
        return out

    def _seed_entidades(self):
        data = [
            ("9852115", "VICENTE SOLER MUNGUÍA", "Guatemala", "medio"),
            ("12345678", "Distribuidora Me Llega, S.A.", "Quetzaltenango", "bajo"),
            ("87654321", "Ingenio Palo Gordo, S.A.", "Escuintla", "alto"),
            ("55667789", "Helvetia Centroamérica", "Ciudad de Guatemala", "bajo"),
            ("99887765", "Corporación Mogori", "Mixco", "medio"),
        ]
        out = {}
        for nit, nombre, ciudad, riesgo in data:
            obj, _ = Entidad.objects.update_or_create(
                nit=nit,
                defaults={
                    "nombre": nombre,
                    "tipo_entidad": Entidad.TIPO_CLIENTE,
                    "ciudad": ciudad,
                    "categoria_riesgo": riesgo,
                    "pais": "Guatemala",
                    "activo": True,
                    "origen": DEMO_ORIGIN,
                    "email": f"contacto@{nit[:6]}.demo.gt",
                    "telefono": "5025550101",
                },
            )
            out[nit] = obj
        return out

    def _seed_contactos(self, entidades):
        samples = [
            ("9852115", "María Soler", "maria.soler@demo.gt", "Gerente General"),
            ("12345678", "Juan Pérez", "jperez@demo.gt", "CFO"),
            ("87654321", "Ana Morales", "ana.morales@demo.gt", "Tesorería"),
            ("55667789", "Carlos Ruiz", "cruiz@demo.gt", "Director Comercial"),
        ]
        for nit, nombre, email, cargo in samples:
            ent = entidades[nit]
            Contacto.objects.update_or_create(
                entidad=ent,
                email=email,
                defaults={
                    "nombre": nombre,
                    "cargo": cargo,
                    "es_contacto_operativo": True,
                    "activo": True,
                },
            )

    def _seed_relaciones(self, entidades, productos, unidades):
        pairs = [
            ("9852115", "LEASING", "LEASING"),
            ("87654321", "LEASING", "LEASING"),
            ("12345678", "FACTORING", "FACTORING"),
        ]
        for nit, prod_code, un_code in pairs:
            RelacionEntidadProducto.objects.update_or_create(
                entidad=entidades[nit],
                producto=productos[prod_code],
                defaults={
                    "unidad_negocio": unidades[un_code],
                    "estado": "activo",
                    "moneda": "GTQ",
                },
            )

    def _seed_crm(self, entidades, user):
        ent = entidades["9852115"]
        Interaccion.objects.update_or_create(
            entidad=ent,
            resumen="Revisión cartera leasing Q2",
            defaults={
                "fecha": date.today() - timedelta(days=5),
                "tipo_interaccion": "reunion",
                "resultado": "Cliente confirma envío de EEFF.",
                "usuario": user,
                "notas": "Registro demo",
            },
        )
        Interaccion.objects.update_or_create(
            entidad=entidades["87654321"],
            resumen="Llamada seguimiento mora",
            defaults={
                "fecha": date.today() - timedelta(days=2),
                "tipo_interaccion": "llamada",
                "resultado": "Compromiso de pago parcial.",
                "seguimiento_requerido": True,
                "usuario": user,
                "notas": "Registro demo",
            },
        )
        Tarea.objects.update_or_create(
            entidad=ent,
            descripcion="Enviar estados financieros actualizados",
            defaults={
                "fecha_limite": date.today() + timedelta(days=7),
                "estado": "pendiente",
                "prioridad": "alta",
                "asignado_a": user,
                "notas": "Tarea demo",
            },
        )
        Tarea.objects.update_or_create(
            entidad=entidades["12345678"],
            descripcion="Agendar visita comercial factoraje",
            defaults={
                "fecha_limite": date.today() + timedelta(days=14),
                "estado": "pendiente",
                "prioridad": "media",
                "notas": "Tarea demo",
            },
        )

    def _seed_import_batches(self, user):
        specs = [
            ("demo_seed_crm", "crm", "entidades_clientes", "demo_crm_entidades.csv", 5),
            ("demo_seed_risk", "risk", "snapshots_leasing", "demo_leasing_mayo.xlsx", 8),
            ("demo_seed_pgo", "pgo", "tickets", "demo_tickets_ti.xlsx", 12),
        ]
        batches = {}
        for hash_key, modulo, tipo, nombre, validas in specs:
            batch, _ = DataImportBatch.objects.update_or_create(
                archivo_hash=hash_key,
                defaults={
                    "modulo": modulo,
                    "tipo_importacion": tipo,
                    "archivo_nombre": nombre,
                    "archivo_ruta": "uploads/demo",
                    "usuario": user,
                    "filas_leidas": validas,
                    "filas_validas": validas,
                    "filas_error": 0,
                    "estado": DataImportBatch.ESTADO_OK,
                    "observaciones": "Lote simulado — seed_wcg_demo",
                },
            )
            batches[modulo] = batch
        return batches

    def _seed_risk(self, entidades, productos, unidades, batch):
        ops_data = [
            ("9852115", "PG01260302", "LEASING", 45, Decimal("125000"), Decimal("42000")),
            ("87654321", "LG01260115", "LEASING", 62, Decimal("890000"), Decimal("120000")),
            ("12345678", "FC01260288", "FACTORING", 0, Decimal("55000"), Decimal("0")),
        ]
        operaciones = {}
        for nit, codigo_op, prod, mora, capital, vencido in ops_data:
            ent = entidades[nit]
            op, _ = RiskOperacion.objects.update_or_create(
                entidad=ent,
                codigo_operacion=codigo_op,
                defaults={
                    "producto": productos[prod],
                    "unidad_negocio": unidades[prod],
                    "moneda": "GTQ",
                    "estado": "vigente",
                    "notas": "Operación demo",
                },
            )
            operaciones[codigo_op] = op
            for offset, mora_i, vencido_i in [(60, max(mora - 15, 0), max(vencido - 5000, 0)), (30, mora, vencido)]:
                snap_date = date(2026, 5, 31) - timedelta(days=offset)
                RiskOperationSnapshot.objects.update_or_create(
                    operacion=op,
                    fecha_snapshot=snap_date,
                    defaults={
                        "entidad": ent,
                        "estado_operacion": "vigente",
                        "producto_nombre_raw": prod.title(),
                        "capital_balance": capital,
                        "past_due_balance": vencido_i,
                        "due_days": mora_i,
                        "monthly_rent": Decimal("8500"),
                        "archivo_origen": "demo_seed",
                        "import_batch": batch,
                    },
                )
        return operaciones

    def _seed_eeff(self, entidades, batch):
        cuts = [
            ("9852115", date(2025, 12, 31), Decimal("2500000"), Decimal("180000")),
            ("87654321", date(2025, 12, 31), Decimal("8900000"), Decimal("420000")),
        ]
        for nit, corte, ventas, utilidad in cuts:
            EstadoFinanciero.objects.update_or_create(
                entidad=entidades[nit],
                fecha_corte=corte,
                defaults={
                    "ventas": ventas,
                    "utilidad_neta": utilidad,
                    "patrimonio": ventas * Decimal("0.35"),
                    "ebitda": utilidad * Decimal("1.2"),
                    "observaciones": "EEFF demo",
                    "import_batch": batch,
                },
            )

    def _seed_alertas(self, entidades, operaciones):
        op = operaciones.get("LG01260115")
        if not op:
            return
        RiskAlerta.objects.update_or_create(
            entidad=entidades["87654321"],
            operacion=op,
            tipo_alerta="mora",
            defaults={
                "fecha_alerta": date.today(),
                "severidad": "alta",
                "mensaje": "Días de atraso superiores a 60 — seguimiento cobranza.",
                "activa": True,
                "origen": DEMO_ORIGIN,
            },
        )

    def _seed_tickets(self, unidades, user, batch):
        now = timezone.now()
        samples = [
            ("TI-DEMO-001", "VPN no conecta", "cerrado", "alta", 18, True),
            ("TI-DEMO-002", "Nuevo usuario CRM", "cerrado", "media", 36, True),
            ("TI-DEMO-003", "Impresora piso 3", "en_proceso", "baja", None, False),
            ("TI-DEMO-004", "Error reporte PGO", "abierto", "alta", None, False),
            ("TI-DEMO-005", "Correo bloqueado", "cerrado", "media", 40, True),
            ("TI-DEMO-006", "Acceso Balón de Riesgo", "cerrado", "media", 12, True),
            ("TI-DEMO-007", "Lentitud de red", "en_proceso", "alta", None, False),
            ("TI-DEMO-008", "Backup fallido", "abierto", "alta", None, False),
        ]
        for i, (tid, titulo, estado, prioridad, horas, sla_ok) in enumerate(samples):
            apertura = now - timedelta(days=20 - i)
            cierre = apertura + timedelta(hours=horas) if horas else None
            if estado == "cerrado" and not cierre:
                cierre = apertura + timedelta(hours=24)
            duracion = Decimal(str(horas)) if horas else None
            PgoTicket.objects.update_or_create(
                ticket_externo_id=tid,
                defaults={
                    "titulo": titulo,
                    "estado_raw": estado.upper(),
                    "estado_normalizado": estado,
                    "prioridad": prioridad,
                    "departamento": "Tecnología",
                    "sistema": "Helpdesk WCG",
                    "usuario_solicita": "Usuario demo",
                    "correo_solicita": "usuario@wcg.demo.gt",
                    "fecha_apertura": apertura,
                    "fecha_cierre": cierre,
                    "fecha_registro": apertura,
                    "anio_mes": apertura.strftime("%Y-%m"),
                    "duracion_horas": duracion,
                    "sla_horas": Decimal("48"),
                    "sla_cumplido": sla_ok,
                    "unidad_negocio": unidades["TI"],
                    "responsable": user,
                    "import_batch": batch,
                    "solucion": "Resuelto en demo" if estado == "cerrado" else "",
                },
            )
