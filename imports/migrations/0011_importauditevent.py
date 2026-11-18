# Generated manually for PGC reload program phase 1

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("imports", "0010_investment_decimal_precision"),
    ]

    operations = [
        migrations.CreateModel(
            name="ImportAuditEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("file_path_key", models.CharField(max_length=512)),
                ("file_available", models.BooleanField(default=False)),
                ("loaded_at", models.DateTimeField(auto_now_add=True)),
                ("success", models.BooleanField(default=False)),
                ("error_message", models.TextField(blank=True)),
                (
                    "source",
                    models.CharField(
                        choices=[
                            ("manual", "Manual (usuario UI)"),
                            ("ops", "Operaciones / CLI"),
                            ("IA", "Automatización / IA"),
                        ],
                        default="ops",
                        max_length=20,
                    ),
                ),
                ("import_tipo", models.CharField(blank=True, max_length=50)),
                ("detail_json", models.JSONField(blank=True, default=dict)),
                (
                    "file_upload",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="audit_events",
                        to="imports.fileupload",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="import_audit_events",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Evento de auditoría de importación",
                "verbose_name_plural": "Eventos de auditoría de importación",
                "ordering": ["-loaded_at"],
            },
        ),
        migrations.AddIndex(
            model_name="importauditevent",
            index=models.Index(
                fields=["file_path_key", "loaded_at"],
                name="imports_imp_file_pa_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="importauditevent",
            index=models.Index(
                fields=["success", "loaded_at"],
                name="imports_imp_success_idx",
            ),
        ),
    ]