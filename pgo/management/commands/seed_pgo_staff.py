"""Carga o actualiza contactos staff PGO (directorio capturas)."""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from pgo.models import PgoStaffMember

User = get_user_model()

# email, full_name, department, role_notes, wcg_username, is_authorized
STAFF_ROWS: list[tuple[str, str, str, str, str, bool]] = [
    (
        "fgonzalez@workingcapitalsa.com",
        "Francisco Arnoldo González Ardón",
        PgoStaffMember.DEPT_TI,
        "",
        "",
        False,
    ),
    (
        "rluther@workingcapitalsa.com",
        "Alexander Luther",
        PgoStaffMember.DEPT_PENDIENTE,
        "",
        "",
        False,
    ),
    (
        "aa@stanfordalumni.org",
        "Armando Amado",
        PgoStaffMember.DEPT_DIRECCION,
        "Owner / usuario principal plataforma",
        "caa",
        True,
    ),
    (
        "cchacon@workingcapitalsa.com",
        "Celeste Eugenia Chacón Flores",
        PgoStaffMember.DEPT_LEGAL,
        "Capturas Legal (garantías, acreedores)",
        "Celeste",
        True,
    ),
    (
        "csamayoa@workingcapitalsa.com",
        "Cindy Gabriela Samayoa Pérez",
        PgoStaffMember.DEPT_FINANZAS,
        "Finanzas y Riesgos — capturas pendientes",
        "csamayoa",
        False,
    ),
    (
        "esazo@workingcapitalsa.com",
        "Erick Alfonso Sazo Pérez",
        PgoStaffMember.DEPT_LEGAL,
        "Apoyo Legal (garantías mobiliarias)",
        "Erick",
        True,
    ),
    (
        "eiriarte@workingcapitalsa.com",
        "Estuardo Iriarte",
        PgoStaffMember.DEPT_PENDIENTE,
        "",
        "",
        False,
    ),
    (
        "gfuentes@workingcapitalsa.com",
        "Gelvin Obil Fuentes Ardiano",
        PgoStaffMember.DEPT_FINANZAS,
        "",
        "",
        False,
    ),
    (
        "gsoler@workingcapitalsa.com",
        "Guillermo Soler Munguia",
        PgoStaffMember.DEPT_DIRECCION,
        "CEO",
        "",
        False,
    ),
    (
        "jherrera@workingcapitalsa.com",
        "Jennifer Daniela Herrera Cortez",
        PgoStaffMember.DEPT_PENDIENTE,
        "",
        "",
        False,
    ),
    (
        "jmartinez@workingcapitalsa.com",
        "José Augusto Martínez Ramírez",
        PgoStaffMember.DEPT_TI,
        "Dirige TI y Finanzas",
        "",
        False,
    ),
    (
        "jvelasquez@workingcapitalsa.com",
        "José Roberto Velásquez Pineda",
        PgoStaffMember.DEPT_FINANZAS,
        "Finanzas senior; capturas Operaciones (cronograma, reportes día 7)",
        "jvelasquez",
        True,
    ),
    (
        "jsanchez@workingcapitalsa.com",
        "Josseline Sánchez Marroquín",
        PgoStaffMember.DEPT_PENDIENTE,
        "",
        "",
        False,
    ),
    (
        "lcastillo@workingcapitalsa.com",
        "Lisbeth Zuseth Castillo Moraga",
        PgoStaffMember.DEPT_PENDIENTE,
        "",
        "",
        False,
    ),
    (
        "sjochola@workingcapitalsa.com",
        "Melody Jochola",
        PgoStaffMember.DEPT_PENDIENTE,
        "",
        "",
        False,
    ),
    (
        "srodas@workingcapitalsa.com",
        "Sergio Alejandro Rodas Romero",
        PgoStaffMember.DEPT_TI,
        "ArchivosPGO, datos; captura TI backup NAS",
        "srodas",
        True,
    ),
    (
        "ypalacios@workingcapitalsa.com",
        "Yeimi Eloisa Palacios Mohr",
        PgoStaffMember.DEPT_PENDIENTE,
        "",
        "",
        False,
    ),
    (
        "gchinchilla@workingcapitalsa.com",
        "Gildardo José Chinchilla Corado",
        PgoStaffMember.DEPT_FINANZAS,
        "",
        "",
        False,
    ),
]


def _link_user(member: PgoStaffMember) -> None:
    if member.user_id:
        return
    candidates: list[User] = []
    if member.wcg_username:
        candidates = list(User.objects.filter(username__iexact=member.wcg_username))
    if not candidates:
        candidates = list(User.objects.filter(email__iexact=member.email))
    if len(candidates) == 1:
        member.user = candidates[0]
        member.save(update_fields=["user", "updated_at"])


class Command(BaseCommand):
    help = "Sembra o actualiza los 18 contactos staff PGO (clave: email)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--link-users",
            action="store_true",
            help="Vincula user FK si hay un único User por wcg_username o email.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        created = updated = 0
        for email, full_name, department, role_notes, wcg_username, is_authorized in STAFF_ROWS:
            defaults = {
                "full_name": full_name,
                "department": department,
                "role_notes": role_notes,
            }
            if wcg_username:
                defaults["wcg_username"] = wcg_username
            obj, was_created = PgoStaffMember.objects.update_or_create(
                email=email,
                defaults=defaults,
            )
            if was_created:
                obj.is_authorized = is_authorized
                obj.is_active = True
                obj.save(update_fields=["is_authorized", "is_active", "updated_at"])
                created += 1
            else:
                updated += 1
            if options["link_users"]:
                _link_user(obj)

        self.stdout.write(
            self.style.SUCCESS(
                f"PgoStaffMember: creados={created} actualizados={updated} total={len(STAFF_ROWS)}"
            )
        )
