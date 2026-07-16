"""
Importa archivos reales WCG desde data/wcg/ (si existen).
Ejecutar: python manage.py import_wcg_data
"""

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand

from core.wcg_paths import (
    CRM_INFO_CLIENTES,
    PGO_ANALISIS_TI,
    PGO_ARCHIVOS,
    PGO_TICKETS_CONTROL,
    RISK_LEASING_DB,
    resolve_data_file,
)
from crm import services as crm_services
from pgo import services as pgo_services
from pgo.periodo import recalculate_pgo_periodos
from risk import services as risk_services

User = get_user_model()

IMPORTERS = [
    (CRM_INFO_CLIENTES, crm_services.import_infoclientes_wcg),
    (RISK_LEASING_DB, risk_services.import_leasing_database),
    (PGO_ARCHIVOS, pgo_services.import_archivos_catalogo),
    (PGO_TICKETS_CONTROL, pgo_services.import_tickets),
    (PGO_ANALISIS_TI, pgo_services.import_tickets),
]


class Command(BaseCommand):
    help = "Importa archivos de datos WCG desde data/wcg/"

    def handle(self, *args, **options):
        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not user:
            self.stderr.write("No hay usuario en BD. Cree uno primero.")
            return
        for filename, importer in IMPORTERS:
            path = resolve_data_file(filename)
            if not path:
                self.stdout.write(self.style.WARNING(f"SKIP (no existe): {filename}"))
                continue
            content = path.read_bytes()
            upload = SimpleUploadedFile(path.name, content)
            batch = importer(user, upload)
            self.stdout.write(
                f"{filename}: {batch.status} — "
                f"creados={batch.creados} actualizados={batch.actualizados} errores={batch.errores}"
            )
            if batch.log_texto:
                self.stdout.write(batch.log_texto[:500])
        recalculate_pgo_periodos()
        self.stdout.write(self.style.SUCCESS("import_wcg_data finalizado."))
