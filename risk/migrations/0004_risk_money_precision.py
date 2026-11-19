from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("risk", "0003_evaluacion_plantillas"),
    ]

    operations = [
        migrations.AlterField(
            model_name="estadofinanciero",
            name="exposicion",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name="estadofinanciero",
            name="saldo_total",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
        migrations.AlterField(
            model_name="pagorealizado",
            name="monto",
            field=models.DecimalField(decimal_places=6, max_digits=18),
        ),
        migrations.AlterField(
            model_name="programacionpago",
            name="monto",
            field=models.DecimalField(decimal_places=6, max_digits=18),
        ),
        migrations.AlterField(
            model_name="riskoperationsnapshot",
            name="monto_exigible",
            field=models.DecimalField(
                decimal_places=6,
                default=0,
                help_text="Monto vencido/exigible al momento del snapshot.",
                max_digits=18,
            ),
        ),
        migrations.AlterField(
            model_name="riskoperationsnapshot",
            name="saldo",
            field=models.DecimalField(decimal_places=6, default=0, max_digits=18),
        ),
    ]