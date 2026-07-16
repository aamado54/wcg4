from django.apps import AppConfig


class LegacyPgc1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.legacy_pgc1"
    label = "wcgone_legacy_pgc1"
    verbose_name = "PGC Legado"
