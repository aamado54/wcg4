"""Rutas estándar de archivos de datos WCG (fuera del código de negocio)."""

from pathlib import Path

from django.conf import settings

# Directorios donde se buscan archivos reales (en orden).
WCG_DATA_DIRS = [
    settings.BASE_DIR / "data" / "wcg",
    settings.BASE_DIR.parent / "data" / "wcg",
]

CRM_INFO_CLIENTES = "crm datos - InfoClientesWCG para CRM.csv"
RISK_LEASING_DB = (
    "balon datos - Ejemplo de datos Riesgo al 31-mayo para una operacion - Base de datos Leasing.xlsx"
)
PGO_ARCHIVOS = "pgo datos - Archivos para PGO.csv"
PGO_TICKETS_CONTROL = "pgo datos - control de tickets marzo abril y mayo 2026 para PGO.xlsx"
PGO_ANALISIS_TI = "pgo ejemplo del analisis - PGO - TI Q22026.xlsx"


def resolve_data_file(filename: str) -> Path | None:
    for base in WCG_DATA_DIRS:
        path = base / filename
        if path.is_file():
            return path
    return None
