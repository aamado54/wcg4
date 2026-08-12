from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imports", "0006_newclientimportheader_file_upload_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="newclientimportrow",
            name="interest_rate",
            field=models.DecimalField(
                blank=True,
                decimal_places=4,
                help_text="Porcentaje del archivo. Investment = anual; Factoraje/Leasing = mensual.",
                max_digits=8,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="newclientimportrow",
            name="rate_basis",
            field=models.CharField(
                blank=True,
                choices=[("annual", "Anual"), ("monthly", "Mensual")],
                default="",
                max_length=12,
            ),
        ),
    ]
