from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pgc", "0007_tv_live_chart_persistence"),
    ]

    operations = [
        migrations.AddField(
            model_name="monthlytarget",
            name="presupuesto_gtq",
            field=models.DecimalField(
                blank=True,
                decimal_places=4,
                help_text="Presupuesto de comisiones en GTQ (hoja Objetivos), solo INGRESOS.",
                max_digits=20,
                null=True,
            ),
        ),
    ]
