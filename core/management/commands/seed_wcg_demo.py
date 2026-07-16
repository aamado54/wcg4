"""
Carga demo WCG One: unidades, entidades, contactos, risk snapshots y tickets PGO.
Ejecutar: python manage.py seed_wcg_demo
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import UNE
from core.wcg_models import Contacto, Entidad, Producto, RelacionEntidadProducto, UnidadNegocio
from crm.models import Interaccion, Tarea
from pgo.models import Ticket
from pgo.periodo import recalculate_pgo_periodos
from risk.models import RiskOperationSnapshot

User = get_user_model()


class Command(BaseCommand):
    help = "Carga datos demo para CRM, Risk y PGO (sin depender de imports externos)"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Sembrando WCG One demo...")
        unidades = self._seed_unidades()
        productos = self._seed_productos(unidades)
        entidades = self._seed_entidades(unidades)
        self._seed_contactos(entidades)
        self._seed_relaciones(entidades, productos)
        self._seed_crm_activity(entidades)
        self._seed_risk(entidades, productos)
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        self._seed_tickets(entidades, unidades, user)
        recalculate_pgo_periodos()
        self.stdout.write(self.style.SUCCESS(
            f"Demo OK: {Entidad.objects.count()} entidades, "
            f"{RiskOperationSnapshot.objects.count()} snapshots, "
            f"{Ticket.objects.count()} tickets"
        ))

    def _seed_unidades(self):
        mapping = [
            ("FACTORING", "Factoraje", "FACTORING"),
            ("LEASING", "Leasing", "LEASING"),
            ("INSURANCE", "Insurance", "INSURANCE"),
            ("INVESTMENT", "Inversiones", "INVESTMENT"),
            ("TI", "Tecnología / TI", None),
        ]
        result = {}
        for code, nombre, une_code in mapping:
            une = UNE.objects.filter(code=une_code).first() if une_code else None
            obj, _ = UnidadNegocio.objects.update_or_create(
                code=code,
                defaults={"nombre": nombre, "une_pgc": une, "activa": True},
            )
            result[code] = obj
        return result

    def _seed_productos(self, unidades):
        data = [
            ("LEASING", "Leasing operativo", "LEASING"),
            ("FACTORING", "Factoraje", "FACTORING"),
        ]
        out = {}
        for code, nombre, un_code in data:
            obj, _ = Producto.objects.update_or_create(
                codigo=code,
                defaults={"nombre": nombre, "unidad_negocio": unidades[un_code], "activo": True},
            )
            out[code] = obj
        return out

    def _seed_entidades(self, unidades):
        data = [
            ("9852115", "VICENTE SOLER MUNGUÍA", "9852115", "LEASING"),
            ("DEMO002", "Distribuidora Me Llega, S.A.", "1234567-8", "FACTORING"),
            ("DEMO003", "Ingenio Palo Gordo, S.A.", "8765432-1", "LEASING"),
            ("DEMO004", "Helvetia Centroamérica", "5566778-9", "INSURANCE"),
            ("DEMO005", "Corporación Mogori", "9988776-5", "INVESTMENT"),
        ]
        out = {}
        for codigo, nombre, nit, un_code in data:
            obj, _ = Entidad.objects.update_or_create(
                codigo=codigo,
                defaults={
                    "nombre": nombre,
                    "nit": nit,
                    "tipo": Entidad.TIPO_CLIENTE,
                    "unidad_negocio": unidades[un_code],
                    "activa": True,
                },
            )
            out[codigo] = obj
        return out

    def _seed_contactos(self, entidades):
        samples = [
            ("9852115", "María Soler", "maria@soler.gt", "Gerente General"),
            ("DEMO002", "Juan Pérez", "jperez@melega.gt", "CFO"),
            ("DEMO003", "Ana Morales", "ana@palogordo.gt", "Tesorería"),
        ]
        for codigo, nombre, email, cargo in samples:
            ent = entidades[codigo]
            Contacto.objects.update_or_create(
                entidad=ent,
                email=email,
                defaults={"nombre": nombre, "cargo": cargo, "es_principal": True, "activo": True},
            )

    def _seed_relaciones(self, entidades, productos):
        RelacionEntidadProducto.objects.update_or_create(
            entidad=entidades["9852115"],
            producto=productos["LEASING"],
            defaults={"estado": RelacionEntidadProducto.ESTADO_ACTIVO},
        )

    def _seed_crm_activity(self, entidades):
        user = User.objects.filter(is_superuser=True).first()
        now = timezone.now()
        ent = entidades["9852115"]
        if not ent.interacciones.exists():
            Interaccion.objects.create(
                entidad=ent,
                tipo=Interaccion.TIPO_REUNION,
                asunto="Revisión cartera leasing",
                descripcion="Seguimiento trimestral",
                fecha=now - timedelta(days=3),
                usuario=user,
            )
        if not ent.tareas.exists():
            Tarea.objects.create(
                entidad=ent,
                titulo="Enviar estados financieros actualizados",
                fecha_vencimiento=date.today() + timedelta(days=7),
                estado=Tarea.ESTADO_PENDIENTE,
                asignado_a=user,
            )

    def _seed_risk(self, entidades, productos):
        base = date(2026, 5, 31)
        ops = [
            ("9852115", "PG01260302", 45, Decimal("125000.00"), Decimal("42000.00"), True),
            ("DEMO003", "LG01260115", 62, Decimal("890000.00"), Decimal("120000.00"), True),
            ("DEMO002", "FC01260288", 12, Decimal("55000.00"), Decimal("0"), False),
        ]
        for codigo, ref, mora, saldo, exigible, alerta in ops:
            ent = entidades[codigo]
            nivel = RiskOperationSnapshot.NIVEL_ALTO if mora >= 30 else RiskOperationSnapshot.NIVEL_BAJO
            RiskOperationSnapshot.objects.update_or_create(
                entidad=ent,
                referencia_operacion=ref,
                fecha_snapshot=base,
                defaults={
                    "producto": productos.get("LEASING") or productos.get("FACTORING"),
                    "nivel_riesgo": nivel,
                    "dias_mora": mora,
                    "saldo": saldo,
                    "monto_exigible": exigible,
                    "alerta": alerta,
                    "detalle": "Snapshot demo mayo 2026",
                },
            )

    def _seed_tickets(self, entidades, unidades, user):
        now = timezone.now()
        samples = [
            ("TI-2026-001", "VPN no conecta", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_ALTA, 24, 18),
            ("TI-2026-002", "Nuevo usuario CRM", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 36),
            ("TI-2026-003", "Impresora piso 3", Ticket.ESTADO_EN_PROCESO, Ticket.PRIORIDAD_BAJA, 72, None),
            ("TI-2026-004", "Error reporte PGO", Ticket.ESTADO_ABIERTO, Ticket.PRIORIDAD_ALTA, 48, None),
            ("TI-2026-005", "Correo bloqueado", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 40),
            ("TI-2026-006", "Acceso Balón Riesgo", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 12),
            ("TI-2026-007", "Lentitud red", Ticket.ESTADO_EN_PROCESO, Ticket.PRIORIDAD_ALTA, 24, None),
            ("TI-2026-008", "Backup fallido", Ticket.ESTADO_ABIERTO, Ticket.PRIORIDAD_ALTA, 24, None),
            ("TI-2026-009", "Licencia Office", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_BAJA, 72, 60),
            ("TI-2026-010", "Actualizar antivirus", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_MEDIA, 48, 20),
            ("TI-2026-011", "Solicitud laptop", Ticket.ESTADO_ABIERTO, Ticket.PRIORIDAD_MEDIA, 48, None),
            ("TI-2026-012", "Reset MFA", Ticket.ESTADO_CERRADO, Ticket.PRIORIDAD_ALTA, 24, 6),
        ]
        for i, (codigo, titulo, estado, prioridad, sla, horas_cierre) in enumerate(samples):
            apertura = now - timedelta(days=30 - i)
            cierre = apertura + timedelta(hours=horas_cierre) if horas_cierre else None
            if estado == Ticket.ESTADO_CERRADO and not cierre:
                cierre = apertura + timedelta(hours=sla - 2)
            Ticket.objects.update_or_create(
                codigo=codigo,
                defaults={
                    "titulo": titulo,
                    "descripcion": f"Ticket demo {codigo}",
                    "entidad": entidades.get("DEMO004"),
                    "unidad_negocio": unidades["TI"],
                    "estado": estado,
                    "prioridad": prioridad,
                    "asignado_a": user,
                    "fecha_apertura": apertura,
                    "fecha_cierre": cierre,
                    "sla_horas": sla,
                },
            )
