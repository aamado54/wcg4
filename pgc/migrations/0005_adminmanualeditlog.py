import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pgc", "0004_rename_calculationnote_monthlymetricscore_calculation_note_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminManualEditLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("year", models.PositiveIntegerField()),
                ("month", models.PositiveIntegerField()),
                (
                    "entity_type",
                    models.CharField(
                        choices=[
                            ("target", "Meta mensual"),
                            ("result", "Resultado mensual"),
                            ("requirement", "Requerimiento manual"),
                            ("fx", "Tipo de cambio"),
                            ("alias", "Alias UNE"),
                            ("new_client_row", "Fila cliente nuevo"),
                            ("cross_sale_row", "Fila venta cruzada"),
                            ("period_note", "Nota del período"),
                        ],
                        max_length=30,
                    ),
                ),
                ("entity_id", models.PositiveIntegerField(blank=True, null=True)),
                ("field_name", models.CharField(max_length=100)),
                ("old_value", models.TextField(blank=True)),
                ("new_value", models.TextField(blank=True)),
                ("reason", models.TextField(blank=True)),
                (
                    "edited_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="admin_manual_edits",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Bitácora de edición manual",
                "verbose_name_plural": "Bitácora de ediciones manuales",
                "ordering": ["-created_at"],
            },
        ),
    ]
