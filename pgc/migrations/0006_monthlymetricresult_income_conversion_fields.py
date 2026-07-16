# Generated manually for INGRESOS GTQ→USD capture trail.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pgc", "0005_adminmanualeditlog"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monthlymetricresult",
            name="measured_value",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=20, null=True
            ),
        ),
        migrations.AddField(
            model_name="monthlymetricresult",
            name="source_currency",
            field=models.CharField(blank=True, default="", max_length=3),
        ),
        migrations.AddField(
            model_name="monthlymetricresult",
            name="source_value",
            field=models.DecimalField(
                blank=True, decimal_places=8, max_digits=20, null=True
            ),
        ),
        migrations.AddField(
            model_name="monthlymetricresult",
            name="exchange_rate_used",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=12, null=True
            ),
        ),
        migrations.AddField(
            model_name="monthlymetricresult",
            name="conversion_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("NATIVE_USD", "USD nativo / legado"),
                    ("CONVERTED", "Convertido GTQ→USD"),
                    ("MISSING_FX", "Sin tipo de cambio"),
                    ("STALE_FX", "TC desactualizado"),
                ],
                default="",
                max_length=20,
            ),
        ),
    ]
