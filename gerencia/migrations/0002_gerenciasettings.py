from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("gerencia", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GerenciaSettings",
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
                (
                    "strict_gerencial",
                    models.BooleanField(
                        default=False,
                        help_text="Si está activo, 301010106 (acciones preferentes) se trata como pasivo a 1 año.",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="gerencia_settings_updates",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Ajuste Centro Gerencial",
                "verbose_name_plural": "Ajustes Centro Gerencial",
            },
        ),
    ]
