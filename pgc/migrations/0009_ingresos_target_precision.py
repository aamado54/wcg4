# Meta ingresos: alinear target_value con measured_value (6 dec miles USD).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pgc", "0008_monthlytarget_presupuesto_gtq"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monthlymetricresult",
            name="target_value",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=20, null=True
            ),
        ),
        migrations.AlterField(
            model_name="monthlytarget",
            name="reference_annual_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                help_text="Solo referencia; no asigna puntos por sí misma.",
                max_digits=20,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="monthlytarget",
            name="target_value",
            field=models.DecimalField(
                blank=True, decimal_places=6, max_digits=20, null=True
            ),
        ),
    ]