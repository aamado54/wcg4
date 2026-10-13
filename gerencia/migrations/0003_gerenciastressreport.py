from datetime import date

from django.db import migrations, models


def seed_first_report(apps, schema_editor):
    GerenciaStressReport = apps.get_model("gerencia", "GerenciaStressReport")
    base = "wcg BRIEF ejecutivo - Diesel EUA-Guatemala sep-2026"
    GerenciaStressReport.objects.update_or_create(
        slug="diesel-eua-guatemala-sep-2026",
        defaults={
            "fecha": date(2026, 9, 24),
            "tema": "Diesel posible escasez pronta",
            "title": base,
            "pdf_filename": f"{base}.pdf",
            "md_filename": f"{base}.md",
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("gerencia", "0002_gerenciasettings"),
    ]

    operations = [
        migrations.CreateModel(
            name="GerenciaStressReport",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha", models.DateField(db_index=True)),
                ("tema", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=120, unique=True)),
                ("title", models.CharField(help_text="Título del documento (nombre base del archivo).", max_length=255)),
                ("pdf_filename", models.CharField(max_length=255)),
                ("md_filename", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Reporte stress test",
                "verbose_name_plural": "Reportes stress test",
                "ordering": ["-fecha", "-pk"],
            },
        ),
        migrations.RunPython(seed_first_report, migrations.RunPython.noop),
    ]
